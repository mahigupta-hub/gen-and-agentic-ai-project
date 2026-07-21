import json
from .ai_client import ask_ai

def generate_quiz(text):
    prompt = f"""
You are an expert teacher.
Generate 5 multiple-choice questions from these notes.

Rules:
- Each question must have exactly 4 options.
- Give only one correct answer.
- Questions should test deep understanding of the notes.
- YOU MUST OUTPUT STRICTLY IN JSON FORMAT.
- Do not include any intro, outro, explanations, or markdown formatting (like ```json). Just the raw JSON list.

Expected JSON format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "answer": "Option A text"
  }}
]

Notes:

{text}
"""

    raw_response = ask_ai(prompt)
    
    # Clean up the response in case the AI includes markdown blocks by mistake
    cleaned_response = raw_response.strip()
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]
    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]
        
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]
        
    cleaned_response = cleaned_response.strip()

    try:
        # Convert the string into an actual Python dictionary/list
        questions_data = json.loads(cleaned_response)
        return {"questions": questions_data}
    except json.JSONDecodeError:
        # Fallback in case the AI fails to generate valid JSON
        return {"error": "Failed to generate valid quiz format.", "raw_text": raw_response}