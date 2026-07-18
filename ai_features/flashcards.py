from ai_client import ask_ai

def generate_flashcards(text):

    prompt = f"""
You are an AI tutor.

Create 10 flashcards.

Rules:
- Each flashcard must have one Question and one Answer.
- Keep answers short.
- Cover all important concepts.

Notes:

{text}
"""

    return ask_ai(prompt)