import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Increased default max_tokens to 4096 to prevent cut-off responses
def ask_ai(prompt, max_tokens=4096): 
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens # Pass the limit to the API here
    )

    return response.choices[0].message.content