import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


prompt = """
Translate English to Pirate Speak:
English: Hello friend
Pirate: Ahoy matey

English: Where is the treasure?
Pirate:"""

print(ask_gpt(prompt))
