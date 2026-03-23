import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from agents.disease_agent import DiseaseIntelligenceAgent
from agents.stockout_agent import StockoutAgent
from agents.vet_agent import VetBehaviorAgent
from agents.orchestrator import OrchestratorAgent

# -------------------------------
# Scenario Generator
# -------------------------------
def generate_disruption_scenario():
    scenarios = [
        "Outbreak of Foot and Mouth Disease in Brazil affecting cattle",
        "Avian Influenza detected in multiple poultry farms in Ontario",
        "Severe drought in Texas impacting livestock feed supply",
        "Swine Fever outbreak reported in China disrupting pork supply chain",
        "Flooding in Midwest USA affecting veterinary access and drug distribution"
    ]
    return random.choice(scenarios)

# -------------------------------
# UI Title
# -------------------------------
st.title("🐄 Animal Health Risk Intelligence Agent")

# -------------------------------
# Session State Init
# -------------------------------
if "custom_text" not in st.session_state:
    st.session_state.custom_text = "Outbreak of Avian Influenza in Ontario affecting poultry"

# -------------------------------
# User Inputs
# -------------------------------
st.subheader("🔧 Configure Scenario")

# Generate Scenario Button
if st.button("⚡ Generate Scenario"):
    st.session_state.custom_text = generate_disruption_scenario()

# Text Area (bound to session state)
custom_text = st.text_area(
    "Enter Disease Signal (Optional)",
    value=st.session_state.custom_text
)

# Keep session updated
st.session_state.custom_text = custom_text

# Risk selection
risk_option = st.selectbox(
    "Select Risk Scenario",
    ["Auto (Real Logic)", "High Risk", "Medium Risk", "Low Risk"]
)

# Map risk options
risk_map = {
    "High Risk": 0.85,
    "Medium Risk": 0.5,
    "Low Risk": 0.2
}

# -------------------------------
# Run Button
# -------------------------------
if st.button("🚀 Run Analysis"):

    try:
        # Initialize agents
        disease_agent = DiseaseIntelligenceAgent([])
        stockout_agent = StockoutAgent("data/inventory_stock_data.csv")
        vet_agent = VetBehaviorAgent("data/veterinary_behavior_data.csv")

        orchestrator = OrchestratorAgent(
            disease_agent,
            stockout_agent,
            vet_agent
        )

        # Determine forced risk
        forced_risk = risk_map.get(risk_option, None)

        # -------------------------------
        # Run Orchestrator (MAIN FIX)
        # -------------------------------
        result = orchestrator.run(
            custom_text=custom_text,
            forced_risk=forced_risk
        )

        # Debug (can remove later)
        st.write("DEBUG RESULT:", result)

        # -------------------------------
        # Display Results
        # -------------------------------
        if result and isinstance(result, dict):

            st.subheader("📊 Risk Summary")

            st.metric("Risk Score", result.get("risk_score", "N/A"))
            st.write("Risk Level:", result.get("risk_level", "N/A"))
            st.write("Trend:", result.get("trend", "N/A"))

            # Alert
            alert = result.get("alert", {})
            if alert.get("alert"):
                st.error(alert.get("message", "Alert triggered"))
            else:
                st.success("No alerts")

            # Drivers
            st.subheader("🔍 Driver Insights")
            st.json(result.get("drivers", {}))

        else:
            st.error("❌ No valid result returned from orchestrator")

    except Exception as e:
        st.error(f"❌ Error running analysis: {str(e)}")