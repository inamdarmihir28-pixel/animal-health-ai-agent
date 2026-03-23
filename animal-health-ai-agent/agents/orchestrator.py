from utils.memory import load_memory, save_memory
from utils.alert import check_alert


class OrchestratorAgent:
    def __init__(self, disease_agent, stockout_agent, vet_agent):
        self.disease_agent = disease_agent
        self.stockout_agent = stockout_agent
        self.vet_agent = vet_agent

    # -------------------------------
    # Risk Score Calculation
    # -------------------------------
    def compute_risk_score(self, disease, stockout, vet):

        # -------------------------------
        # Disease score (safe handling)
        # -------------------------------
        if isinstance(disease, list):
            disease_score = len(disease) * 0.2
        elif isinstance(disease, dict):
            disease_score = len(disease.keys()) * 0.2
        else:
            disease_score = 0.2 if disease else 0

        # -------------------------------
        # Stockout score (safe handling)
        # -------------------------------
        if isinstance(stockout, dict):
            high_risk_products = stockout.get("high_risk_products", {})
            stockout_score = len(high_risk_products) * 0.05
        else:
            stockout_score = 0

        # -------------------------------
        # Vet behavior score (safe handling)
        # -------------------------------
        if isinstance(vet, dict):
            declining_regions = vet.get("declining_usage_regions", [])
            vet_score = len(declining_regions) * 0.05
        else:
            vet_score = 0

        # -------------------------------
        # Final score
        # -------------------------------
        total = min(1.0, disease_score + stockout_score + vet_score)
        return total

    # -------------------------------
    # Main Execution
    # -------------------------------
    def run(self, custom_text=None, forced_risk=None):

        # -------------------------------
        # Run all agents
        # -------------------------------
        try:
            disease_output = self.disease_agent.run(custom_text=custom_text)
        except Exception:
            disease_output = []

        try:
            stockout_output = self.stockout_agent.analyze()
        except Exception:
            stockout_output = {}

        try:
            vet_output = self.vet_agent.analyze()
        except Exception:
            vet_output = {}

        # -------------------------------
        # Risk Score (with override)
        # -------------------------------
        if forced_risk is not None:
            risk_score = forced_risk
        else:
            risk_score = self.compute_risk_score(
                disease_output,
                stockout_output,
                vet_output
            )

        # -------------------------------
        # Risk Level
        # -------------------------------
        if risk_score > 0.7:
            risk_level = "High"
        elif risk_score > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # -------------------------------
        # Load Memory (previous runs)
        # -------------------------------
        try:
            memory = load_memory()
        except Exception:
            memory = []

        if memory and isinstance(memory, list):
            try:
                last_score = memory[-1].get("risk_score", None)

                if last_score is not None:
                    if risk_score > last_score:
                        trend = "Increasing Risk"
                    elif risk_score < last_score:
                        trend = "Decreasing Risk"
                    else:
                        trend = "Stable"
                else:
                    trend = "No historical data"

            except Exception:
                trend = "No historical data"
        else:
            trend = "No historical data"

        # -------------------------------
        # Alert System
        # -------------------------------
        try:
            alert = check_alert(risk_score)
        except Exception:
            alert = {"alert": False, "message": "Alert system unavailable"}

        # -------------------------------
        # Final Output
        # -------------------------------
        result = {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "trend": trend,
            "alert": alert,
            "drivers": {
                "disease": disease_output,
                "stockout": stockout_output,
                "vet_behavior": vet_output
            },
            "recommended_actions": [
                "Reallocate inventory",
                "Increase vet engagement",
                "Monitor disease outbreaks closely"
            ]
        }

        # -------------------------------
        # Save to Memory
        # -------------------------------
        try:
            save_memory(result)
        except Exception:
            pass

        return result