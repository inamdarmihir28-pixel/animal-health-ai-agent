# 🐄 LLM-powered Decision Intelligence Platform for Canada Animal Health Manufacturers

An AI-powered, multi-agent decision intelligence system designed to proactively identify and manage risks in the animal health ecosystem of Canada.

## 🚨 The Problem

Animal health manufacturers and stakeholders operate in a highly volatile environment driven by:

- Disease outbreaks (e.g., Avian Influenza, Swine Fever)
- Supply chain disruptions and product stockouts
- Shifting veterinary behavior and prescription trends

Today, these signals exist in silos—making it difficult to:

❌ Detect risks early  
❌ Understand cross-functional impact  
❌ Take timely, data-driven action  

## 💡 The Solution

The **Animal Health Risk Intelligence Agent** is a unified, AI-driven system that:

✅ Aggregates signals across disease, supply, and behavior  
✅ Simulates real-world disruption scenarios  
✅ Generates a dynamic risk score and trend  
✅ Triggers alerts and recommended actions  
✅ Generates LLM powered recommendations

👉 Enabling **proactive decision-making instead of reactive firefighting**

---

🧠 Core Capabilities

1. Multi-Agent Intelligence
The system leverages specialized agents:

- **Disease Intelligence Agent**  
  Detects and interprets outbreak signals from unstructured inputs

- **Stockout Risk Agent**  
  Identifies high-risk products based on inventory patterns

- **Veterinary Behavior Agent**  
  Tracks declining usage trends across regions

- **Context sharing with LLM**
  Enables cross-agent reasoning to handle real world data

- **Structured JSON**
  API-ready


---

2. Orchestrator (Decision Engine)

A central **Orchestrator Agent**:

- Combines outputs from all agents  
- Computes a unified **Risk Score (0–1)**  
- Classifies risk as **Low / Medium / High**  
- Tracks **risk trends over time**  
- Triggers **alerts based on thresholds**

3. Architecture Overview

[Web + Data]
     ↓
[Scenario Generator Agent]
     ↓
[Disease Agent (LLM)]
[Stockout Agent]
[Vet Behavior Agent (LLM-enhanced)]
     ↓
[Combined data layer]
     ↓
[Orchestrator]
     ↓
[LLM Decision Engine]
     ↓
[Dynamic Recommendations] (LLM-enhanced)


3. Scenario Simulation (Key Differentiator)

Users can:

- Generate AI-driven disruption scenarios  
- Override risk conditions (High / Medium / Low)  
- Test “what-if” situations  

👉 This transforms the tool from a dashboard into a **decision simulation engine**


4. Explainable Insights

The system provides:

- Key **risk drivers**
- Breakdown across:
  - Disease signals
  - Stockout risks
  - Vet behavior shifts
- Recommended business actions using OpenAI API


## 📊 Business Value

### 🎯 For Animal Health Manufacturers

- Anticipate demand spikes due to outbreaks  
- Prevent revenue loss from stockouts  
- Optimize product allocation across regions  

---

### 📦 For Supply Chain Teams

- Identify high-risk SKUs early  
- Improve inventory planning  
- Reduce operational disruptions  

### 🩺 For Commercial & Field Teams

- Detect declining product adoption  
- Align vet engagement strategies  
- Improve targeting and campaign effectiveness  

---

### 🧠 For Leadership

- Single view of enterprise risk


- Data-backed decision making  
- Faster response to market changes  



## 🧪 How to Test This Project (Step-by-Step)

1. Clone the repo:
```bash
git clone https://github.com/your-username/animal-health-ai-agent.git
cd animal-health-ai-agent

Create virtual environment:
python -m venv agentic_env

Activate:
agentic_env\Scripts\activate   # Windows
source agentic_env/bin/activate  # Mac/Linux

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

Open browser:
http://localhost:8501
