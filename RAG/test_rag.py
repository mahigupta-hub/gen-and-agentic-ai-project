from rag_module import RAGIndex

rag = RAGIndex()
rag.load("saved_index")   

test_questions = [
    "How do plants make food from sunlight?",
    "What powers cellular respiration?",
    "What happens when a force acts on a moving object?",
]

for q in test_questions:
    print(f"\nQ: {q}")
    for match in rag.retrieve(q, k=2):
        print(f"  score={match['score']:.3f} | {match['text'][:80]}...")