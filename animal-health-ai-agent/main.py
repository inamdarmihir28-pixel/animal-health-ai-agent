from agents.disease_agent import DiseaseIntelligenceAgent
from agents.stockout_agent import StockoutAgent
from agents.vet_agent import VetBehaviorAgent
from agents.orchestrator import OrchestratorAgent

disease_sources = [
    "https://animalhealthcanada.ca/",
    "https://cahss.ca/",
    "https://www.canadianveterinarians.net/"
]

disease_agent = DiseaseIntelligenceAgent(disease_sources)
stockout_agent = StockoutAgent("data/inventory_stock_data.csv")
vet_agent = VetBehaviorAgent("data/veterinary_behavior_data.csv")

orchestrator = OrchestratorAgent(disease_agent, stockout_agent, vet_agent)

result = orchestrator.run()

print(result)