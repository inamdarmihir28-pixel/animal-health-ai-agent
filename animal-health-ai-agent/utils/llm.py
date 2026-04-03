import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_api_key():
    # Prefer environment variable for local/dev usage.
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # Fallback to Streamlit secrets when running in Streamlit Cloud.
    try:
        import streamlit as st

        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def _get_client():
    global _client

    if _client is not None:
        return _client

    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Set it in environment variables or Streamlit secrets."
        )

    _client = OpenAI(api_key=api_key)
    return _client


def call_openai(prompt, model=None):
    if not prompt or not str(prompt).strip():
        raise ValueError("Prompt must be a non-empty string.")

    client = _get_client()
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": str(prompt).strip()}
        ]
    )
    return response.choices[0].message.content


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