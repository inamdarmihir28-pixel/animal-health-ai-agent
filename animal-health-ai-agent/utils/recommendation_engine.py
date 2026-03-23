from utils.llm import call_openai

def generate_recommendations(data):

    prompt = f"""
    You are an AI strategist for animal health manufacturers.

    Based on the following data:
    {data}

    Provide:
    1. Region-specific actions
    2. Product-specific recommendations
    3. Clinic-level targeting strategy
    4. Expected business impact

    Return structured JSON.
    """

    return call_openai(prompt)