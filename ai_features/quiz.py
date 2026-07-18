from ai_client import ask_ai

def generate_quiz(text):

    prompt = f"""
You are an expert teacher.

Generate 5 multiple-choice questions from these notes.

Rules:
- Each question should have 4 options (A, B, C, D).
- Give only one correct answer.
- Questions should test understanding.
- Mention the correct answer after each question.

Notes:

{text}
"""

    return ask_ai(prompt)