import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_openai(prompt, model=None):
    if not prompt or not str(prompt).strip():
        raise ValueError("Prompt must be a non-empty string.")

    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=selected_model,
        input=str(prompt).strip(),
    )
    return response.output_text


def extract_disease_info(text):

    prompt = f"""
    Extract structured disease outbreak info from the text below.

    Return ONLY valid JSON with:
    - disease_name
    - date
    - species_affected
    - regions_affected
    - severity
    - government_advisory
    - business_actions

    TEXT:
    {text}
    """

    return call_openai(prompt)