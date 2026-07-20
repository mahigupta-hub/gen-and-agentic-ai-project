"""
RAG Module — Embeddings + Vector Search (FAISS)
=================================================

WHAT THIS FILE DOES:
1. Takes text chunks (from the PDF-processing teammate)
2. Cleans them (drops empty/junk chunks, removes duplicates)
3. Turns each chunk into an "embedding" (a list of numbers representing meaning)
4. Stores those embeddings in a FAISS index (a fast search structure)
5. Given a student's question, finds the most relevant chunks
6. Refuses to return a chunk if it isn't actually relevant enough

HOW THIS FITS THE TEAM CONTRACT:
- Input:  list of chunks like [{"chunk_id": 1, "text": "...", "page": 3}, ...]
          (this comes from your PDF-processing teammate)
- Output: a list of the most relevant chunk texts for a given question
          (this goes to your AI-features teammate, who feeds it to the LLM)

INSTALL FIRST (run this in your terminal):
    pip install sentence-transformers faiss-cpu
"""

import os
import json
import faiss
import numpy as np

# --- 1. NEW: Import the Serverless Inference Client ---
from huggingface_hub import InferenceClient

# -----------------------------------------------------------------------
# STEP 1: Set up the Serverless AI Model
# -----------------------------------------------------------------------
# We define the model name, but we DO NOT download it locally anymore.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# all-MiniLM-L6-v2 always produces vectors of this exact length (384).
EMBEDDING_DIM = 384

# Initialize the Hugging Face client (Zero RAM usage!)
# It automatically picks up the HF_TOKEN from your environment variables.
hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))

DEFAULT_MIN_SCORE = 0.3


class RAGIndex:
    """
    Wraps a FAISS index + the original chunk texts together,
    so we can go from "closest vector" back to "original text".
    """

    def __init__(self):
        self.index = None          # the FAISS index (stores vectors)
        self.chunks = []           # the original text chunks (same order as vectors)

    # ------------------------------------------------------------------
    # Internal helper: clean up raw chunks before we ever embed them
    # ------------------------------------------------------------------
    def _clean_chunks(self, chunks):
        """ Filters out chunks that would silently break or degrade retrieval """
        if not isinstance(chunks, list) or len(chunks) == 0:
            raise ValueError(
                "build_index() expects a non-empty list of chunk dicts, "
                f"got: {type(chunks).__name__} with length "
                f"{len(chunks) if hasattr(chunks, '__len__') else 'unknown'}"
            )

        seen_texts = set()
        cleaned = []
        dropped_empty = 0
        dropped_duplicate = 0

        for i, chunk in enumerate(chunks):
            if not isinstance(chunk, dict) or "text" not in chunk:
                raise ValueError(
                    f"Chunk at position {i} is missing a 'text' key. "
                    f"Every chunk must look like {{'chunk_id': ..., 'text': ..., 'page': ...}}. "
                    f"Got: {chunk!r}"
                )

            text = chunk["text"]
            if text is None or not str(text).strip():
                dropped_empty += 1
                continue

            normalized = str(text).strip()
            if normalized in seen_texts:
                dropped_duplicate += 1
                continue

            seen_texts.add(normalized)
            cleaned.append(chunk)

        if dropped_empty:
            print(f"[RAG] Skipped {dropped_empty} empty/whitespace-only chunk(s).")
        if dropped_duplicate:
            print(f"[RAG] Skipped {dropped_duplicate} duplicate chunk(s).")

        if not cleaned:
            raise ValueError(
                "All chunks were empty or duplicates after cleaning — "
                "nothing left to index. Check the PDF-processing output."
            )

        return cleaned

    def build_index(self, chunks):
        """
        Takes the chunks from PDF processing and builds a searchable index.
        """
        self.chunks = self._clean_chunks(chunks)
        texts = [c["text"] for c in self.chunks]

        # --- 2. NEW: Get embeddings via API instead of local RAM ---
        print(f"[RAG] Generating embeddings via Hugging Face API for {len(texts)} chunks...")
        
        # We process them in a loop to avoid overloading the free API payload limits
        raw_embeddings = []
        for text in texts:
            # Calls Hugging Face servers for a single text chunk
            emb = hf_client.feature_extraction(text, model=MODEL_NAME)
            raw_embeddings.append(emb)

        # Convert the API response into the exact float32 numpy array FAISS needs
        # Output shape: (number_of_chunks, 384)
        embeddings = np.array(raw_embeddings).astype("float32")

        # Normalize vectors so we can use cosine similarity via inner product.
        faiss.normalize_L2(embeddings)

        self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
        self.index.add(embeddings)

        print(f"[RAG] Indexed {len(self.chunks)} chunks (from {len(chunks)} received).")

    def retrieve(self, question, k=3, min_score=DEFAULT_MIN_SCORE):
        """
        Given a student's question, return the top-k most relevant chunks.
        """
        if self.index is None:
            raise ValueError("Index not built yet. Call build_index() or load() first.")

        if not question or not str(question).strip():
            raise ValueError("retrieve() got an empty question.")

        # --- 3. NEW: Get the question embedding via API ---
        raw_q_emb = hf_client.feature_extraction(question, model=MODEL_NAME)
        
        # Convert API response to float32 numpy array. 
        # FAISS expects a 2D array for searches, e.g., shape (1, 384)
        q_vector = np.array([raw_q_emb]).astype("float32")
        
        faiss.normalize_L2(q_vector)

        scores, positions = self.index.search(q_vector, k)

        results = []
        for score, pos in zip(scores[0], positions[0]):
            if pos == -1:
                continue  # FAISS returns -1 if there are fewer than k chunks total
            if score < min_score:
                continue  # not relevant enough -- don't hand this to the LLM
            chunk = self.chunks[pos].copy()
            chunk["score"] = float(score)
            results.append(chunk)

        return results

    def save(self, folder_path):
        """ Saves the FAISS index + chunk data to disk """
        if self.index is None:
            raise ValueError("Nothing to save yet -- call build_index() first.")

        os.makedirs(folder_path, exist_ok=True)

        faiss.write_index(self.index, os.path.join(folder_path, "index.faiss"))

        with open(os.path.join(folder_path, "chunks.json"), "w", encoding="utf-8") as f:
            json.dump(self.chunks, f)

        meta = {"embedding_dim": EMBEDDING_DIM, "model_name": MODEL_NAME}
        with open(os.path.join(folder_path, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f)

        print(f"[RAG] Saved index + {len(self.chunks)} chunks to '{folder_path}/'")

    def load(self, folder_path):
        """ Loads a previously saved index + chunks from disk. """
        index_path = os.path.join(folder_path, "index.faiss")
        chunks_path = os.path.join(folder_path, "chunks.json")
        meta_path = os.path.join(folder_path, "meta.json")

        if not os.path.exists(index_path) or not os.path.exists(chunks_path):
            raise FileNotFoundError(
                f"No saved index found in '{folder_path}/'. "
                "Call build_index() and save() first."
            )

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if meta.get("embedding_dim") != EMBEDDING_DIM:
                raise ValueError(
                    f"Saved index was built with a different embedding model "
                    f"(dim={meta.get('embedding_dim')}) than the one currently "
                    f"loaded (dim={EMBEDDING_DIM}). Delete '{folder_path}/' and "
                    "rebuild the index."
                )

        self.index = faiss.read_index(index_path)

        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"[RAG] Loaded index with {len(self.chunks)} chunks from '{folder_path}/'")

# -----------------------------------------------------------------------
# EXAMPLE / TEST
# -----------------------------------------------------------------------
if __name__ == "__main__":
    INDEX_FOLDER = "saved_index"
    DATA_FILE = "data/sample_chunks.json"

    rag = RAGIndex()

    if os.path.exists(os.path.join(INDEX_FOLDER, "index.faiss")):
        rag.load(INDEX_FOLDER)
    else:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            sample_chunks = json.load(f)
        rag.build_index(sample_chunks)
        rag.save(INDEX_FOLDER)

    test_questions = [
        "How do plants make food from sunlight?",
        "What is the capital of France?",
    ]

    for test_question in test_questions:
        print(f"\nQuestion: {test_question}")
        top_matches = rag.retrieve(test_question, k=2)
        if not top_matches:
            print("  No sufficiently relevant chunks found.")
        else:
            for match in top_matches:
                print(f"  (score={match['score']:.3f}, page={match['page']}) {match['text']}")