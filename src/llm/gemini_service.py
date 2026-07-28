import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(context, question):

    prompt = f"""
You are an AI Research Assistant.

Answer ONLY using the information below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
'I could not find the answer in the uploaded documents.'
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text