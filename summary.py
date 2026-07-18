from ai_client import ask_ai

def generate_summary(text):

    prompt = f"""
You are an expert academic tutor.

Summarize the following notes.

Rules:
- Use simple English.
- Maximum 8 bullet points.
- Highlight important keywords.
- Do not add information that is not present in the notes.
- Make the summary easy for students to revise.

Notes:

{text}
"""

    return ask_ai(prompt)