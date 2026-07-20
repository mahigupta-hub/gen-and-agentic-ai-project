from .ai_client import ask_ai
def answer_question(context, question):

    prompt = f"""
You are an academic tutor.

Answer the question ONLY using the given context.

Context:
{context}

Question:
{question}

Rules:
- Do not use outside knowledge.
- If the answer is not found in the context, reply:
  "I couldn't find this information in the provided notes."
- Keep the answer simple and accurate.
"""

    return ask_ai(prompt, max_tokens=1000)