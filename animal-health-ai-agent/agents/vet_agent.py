from utils.llm import call_openai

def generate_commercial_recommendations(data):

    prompt = f"""
    You are a commercial strategist for animal health manufacturers.

    Based on the data below:
    {data}

    Provide:
    - Clinics to target
    - Products to push
    - Sales strategy
    - Revenue opportunity

    Return structured JSON.
    """

    return call_openai(prompt)

import pandas as pd

class VetBehaviorAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def analyze(self):
        df = self.df.copy()

        # Usage change %
        df["usage_change"] = (
            (df["weekly_usage"] - df["previous_week_usage"]) /
            (df["previous_week_usage"] + 1)
        )

        # Declining usage
        declining = df[df["usage_change"] < -0.3]

        region_decline = (
            declining.groupby(["region", "product"])
            .size()
            .sort_values(ascending=False)
            .head(10)
        )

        # Switching behavior (proxy)
        switching = df[df["usage_change"] < -0.2]
        switching_regions = (
            switching.groupby("region")
            .size()
            .sort_values(ascending=False)
            .head(5)
        )

        declining_usage_regions_dict = {
            f"{region} | {product}": int(value)
            for (region, product), value in region_decline.to_dict().items()
        }
        high_switching_regions_dict = {
            str(region): int(value)
            for region, value in switching_regions.to_dict().items()
        }

        return {
            
            "clinic_insights": [
  {
    "clinic_id": "CL001",
    "region": "Ontario",
    "product": "vaccine_001",
    "trend": "declining",
    "opportunity": "high"
  }
],
            "high_switching_regions": high_switching_regions_dict,
            "recommendations": [
                "Realign salesforce in declining regions",
                "Provide continuing education to veterinarians",
                "Improve technical support",
                "Enhance product quality"
            ]
        }

