"""
RAG Module — Embeddings + Vector Search (FAISS)
=================================================
This is YOUR piece of the AI Tutor project.

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
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------------------------------------------------------
# STEP 1: Load the embedding model
# -----------------------------------------------------------------------
# 'all-MiniLM-L6-v2' is small, free, runs fine on a normal laptop CPU
# (no GPU needed), and is the most commonly used starter model for RAG.
# The first time you run this, it downloads automatically (~80MB).
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# This model always produces vectors of this exact length.
# We use this to sanity-check saved indexes on load (see load() below).
EMBEDDING_DIM = EMBEDDING_MODEL.get_sentence_embedding_dimension()

# If the best match for a question scores below this, we treat it as
# "nothing relevant found" instead of confidently returning a bad answer.
# Cosine similarity ranges roughly -1 to 1; 0.3 is a conservative floor
# for a small model like this one. Tune this after testing real questions.
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
        """
        Filters out chunks that would silently break or degrade retrieval:
        - missing/empty/whitespace-only text
        - exact duplicate text (common with buggy PDF extraction)

        Returns a new, cleaned list. Never modifies the input list.
        """
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

        chunks: list of dicts, e.g.
            [{"chunk_id": 1, "text": "Newton's first law states...", "page": 3}, ...]

        Raises ValueError with a clear message if the input is malformed.
        """
        self.chunks = self._clean_chunks(chunks)

        texts = [c["text"] for c in self.chunks]

        # Turn every chunk of text into a vector (embedding).
        # Output shape: (number_of_chunks, 384) -- 384 numbers per chunk
        # for this particular model.
        embeddings = EMBEDDING_MODEL.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.astype("float32")

        # Normalize vectors so we can use cosine similarity via inner product.
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]        # 384 for this model
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        print(f"[RAG] Indexed {len(self.chunks)} chunks (from {len(chunks)} received).")

    def retrieve(self, question, k=3, min_score=DEFAULT_MIN_SCORE):
        """
        Given a student's question, return the top-k most relevant chunks.

        question: string, e.g. "How does photosynthesis work?"
        k: how many chunks to retrieve (3 is a reasonable default)
        min_score: chunks scoring below this are considered irrelevant and
                   dropped. Pass min_score=0 to disable this filter.

        Returns: list of dicts, same shape as input chunks, most relevant first.
                 Returns an empty list if nothing meets min_score --
                 callers (AI-features teammate) should handle that case,
                 e.g. by saying "I couldn't find that in the material."
        """
        if self.index is None:
            raise ValueError("Index not built yet. Call build_index() or load() first.")

        if not question or not str(question).strip():
            raise ValueError("retrieve() got an empty question.")

        q_vector = EMBEDDING_MODEL.encode([question], convert_to_numpy=True).astype("float32")
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
        """
        Saves the FAISS index + chunk data to disk, so you don't have to
        rebuild (re-embed everything) every time your app starts.

        folder_path: e.g. "saved_index"
        """
        if self.index is None:
            raise ValueError("Nothing to save yet -- call build_index() first.")

        os.makedirs(folder_path, exist_ok=True)

        faiss.write_index(self.index, os.path.join(folder_path, "index.faiss"))

        with open(os.path.join(folder_path, "chunks.json"), "w", encoding="utf-8") as f:
            json.dump(self.chunks, f)

        # Record which embedding model + dimension built this index, so load()
        # can catch the case where someone later swaps embedding models and
        # the old saved index would otherwise fail with a confusing error.
        meta = {"embedding_dim": EMBEDDING_DIM, "model_name": "all-MiniLM-L6-v2"}
        with open(os.path.join(folder_path, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f)

        print(f"[RAG] Saved index + {len(self.chunks)} chunks to '{folder_path}/'")

    def load(self, folder_path):
        """
        Loads a previously saved index + chunks from disk.
        Use this instead of build_index() when you already built it before.
        """
        index_path = os.path.join(folder_path, "index.faiss")
        chunks_path = os.path.join(folder_path, "chunks.json")
        meta_path = os.path.join(folder_path, "meta.json")

        if not os.path.exists(index_path) or not os.path.exists(chunks_path):
            raise FileNotFoundError(
                f"No saved index found in '{folder_path}/'. "
                "Call build_index() and save() first."
            )

        # Guard against loading an index built with a different embedding
        # model -- vector dimensions wouldn't match and FAISS would either
        # error confusingly or silently return garbage results.
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
# EXAMPLE / TEST -- run this file directly to see it work:  python rag_module.py
# -----------------------------------------------------------------------
if __name__ == "__main__":
    INDEX_FOLDER = "saved_index"
    DATA_FILE = "data/sample_chunks.json"

    rag = RAGIndex()

    # If we've already built + saved an index before, just load it (fast).
    # Otherwise, build it from scratch from the sample data (slower, one-time).
    if os.path.exists(os.path.join(INDEX_FOLDER, "index.faiss")):
        rag.load(INDEX_FOLDER)
    else:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            sample_chunks = json.load(f)
        rag.build_index(sample_chunks)
        rag.save(INDEX_FOLDER)

    test_questions = [
        "How do plants make food from sunlight?",
        "What is the capital of France?",   # deliberately irrelevant -- should return nothing
    ]

    for test_question in test_questions:
        print(f"\nQuestion: {test_question}")
        top_matches = rag.retrieve(test_question, k=2)
        if not top_matches:
            print("  No sufficiently relevant chunks found.")
        else:
            for match in top_matches:
                print(f"  (score={match['score']:.3f}, page={match['page']}) {match['text']}")