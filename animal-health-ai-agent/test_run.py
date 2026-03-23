from agents.disease_agent import DiseaseIntelligenceAgent
from agents.stockout_agent import StockoutAgent
from agents.vet_agent import VetBehaviorAgent
from agents.orchestrator import OrchestratorAgent
import json

# -------- INPUT CONFIG -------- #

disease_sources = [
    "https://animalhealthcanada.ca/",
    "https://cahss.ca/"
]

inventory_file = "data/inventory_stock_data.csv"
vet_file = "data/veterinary_behavior_data.csv"

# Optional: override risk threshold for testing
RISK_THRESHOLD = 0.7

# -------- RUN SYSTEM -------- #

disease_agent = DiseaseIntelligenceAgent(disease_sources)
stockout_agent = StockoutAgent(inventory_file)
vet_agent = VetBehaviorAgent(vet_file)

orchestrator = OrchestratorAgent(
    disease_agent,
    stockout_agent,
    vet_agent
)

result = orchestrator.run()

# -------- OUTPUT -------- #

print("\n===== FINAL STRUCTURED OUTPUT =====\n")
print(json.dumps(result, indent=2))