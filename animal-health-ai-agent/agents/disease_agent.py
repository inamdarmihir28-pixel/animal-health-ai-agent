import requests
from bs4 import BeautifulSoup
from utils.llm import extract_disease_info
from datetime import datetime


class DiseaseIntelligenceAgent:
    def __init__(self, sources):
        self.sources = sources

    def fetch_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        except:
            return ""

    def extract_signals(self, text):
        # Rule-based fallback (works without LLM)
        diseases = ["Avian Influenza", "African Swine Fever", "Foot and Mouth Disease"]
        species = ["Poultry", "Swine", "Cattle"]
        regions = ["Ontario", "Alberta", "Quebec", "British Columbia"]

        detected = []

        for disease in diseases:
            if disease.lower() in text.lower():
                detected.append({
                    "disease": disease,
                    "date": str(datetime.today().date()),
                    "species_affected": [s for s in species if s.lower() in text.lower()],
                    "regions_affected": [r for r in regions if r.lower() in text.lower()],
                    "efficacy": "High Risk",
                    "advisory": "Monitor and restrict animal movement",
                    "business_actions": [
                        "Increase inventory in unaffected regions",
                        "Engage veterinarians proactively",
                        "Adjust supply chain logistics"
                    ]
                })

        return detected

    def run(self, custom_text=None):
        # -------------------------------
        # TEST MODE (for UI/demo)
        # -------------------------------
        TEST_MODE = False

        # -------------------------------
        # Step 1: Get Text Input
        # -------------------------------
        if custom_text:
            text = custom_text

        elif TEST_MODE:
            text = "Outbreak of Avian Influenza in Ontario affecting poultry"

        else:
            text = ""
            for url in self.sources:
                text += self.fetch_content(url)

        # -------------------------------
        # Step 2: Extract Signals
        # -------------------------------
        try:
            # Try LLM extraction first
            llm_output = extract_disease_info(text)

            if llm_output:
                return llm_output

        except:
            pass  # fallback to rule-based

        # -------------------------------
        # Step 3: Fallback Logic
        # -------------------------------
        return self.extract_signals(text)