import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60.0,      
    max_retries=2,     
)

# llama-3.1-8b-instant was shut down by Groq on 2026-08-16 so we changed the model
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def ask_ai(prompt, max_tokens=4096):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        # gpt-oss is a reasoning model: reasoning tokens count toward this limit
        max_completion_tokens=max_tokens,
        # keep reasoning short so the answer doesn't get cut off or come back empty
        reasoning_effort="low",
    )

    choice = response.choices[0]
    content = choice.message.content

    if not content or not content.strip():
        raise RuntimeError(
            f"The AI returned an empty response (finish_reason={choice.finish_reason})."
        )

    return content.strip()