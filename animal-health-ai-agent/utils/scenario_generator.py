from utils.llm import call_openai

def generate_disruption_scenario():
    prompt = """
    Generate a realistic animal health disruption scenario in Canada.
    
    Include:
    - Disease outbreak or regulatory change
    - Region
    - Species
    - Business impact
    
    Keep it short and realistic.
    """

    response = call_openai(prompt)
    return response