# AI-Powered-Inventory-Manager
📦 Inventory-AI: Predictive Logistics & Autonomous Decision Engine
Inventory-AI is an end-to-end Decision Intelligence platform that transforms historical sales data into proactive procurement strategies. By integrating Bayesian Time-Series Forecasting, Monte Carlo Risk Simulations, and Automated Negotiation Agents, this system minimizes stockout risks while optimizing warehouse capital allocation.

🚀 Key Features
1. Bayesian Demand Forecasting
Utilizes Meta Prophet to model multi-year demand patterns. Unlike traditional moving averages, this engine:

Accounts for Seasonality (Holidays, Back-to-School cycles).

Incorporates Exogenous Regressors (Price Elasticity and Market Trends).

Provides Uncertainty Quantification (Bayesian credible intervals) to drive risk-based decisions.

2. Probabilistic Risk Assessment
Features a Monte Carlo Simulation Engine that runs 1,000+ "future scenarios" for every SKU. It calculates a mathematical Probability of Stockout, moving away from static safety stock formulas to a dynamic, distribution-aware model.

3. Explainable AI (XAI)
To ensure "Human-in-the-Loop" trust, the system decomposes every forecast into its core components: Trend, Yearly Seasonality, and Weekly Seasonality. This allows users to understand the "Why" behind every AI-generated alert.

4. Autonomous Procurement Agent
When the system detects a critical risk (calculated via Revenue at Risk), it triggers a logic-driven agent to:

Draft a context-aware negotiation email.

Suggest bulk discounts based on financial impact.

Dispatch alerts to vendors via an automated SMTP pipeline.

🛠️ Technical Architecture
Frontend: Streamlit (Strategic Management Dashboard)

Forecasting: Prophet (with Cross-Validation & MAPE tracking)

Simulation: NumPy-based Monte Carlo Engine

📈 Data Science Evaluation Metrics
This project implements rigorous model validation to ensure production readiness:

MAPE (Mean Absolute Percentage Error): Tracks the average deviation of the forecast.

Model Confidence Score: Quantifies the reliability of the AI based on Bayesian uncertainty.

Backtesting: Simulates historical performance to verify model stability across different time horizons.
Optimization: Economic Order Quantity (EOQ) & Uncertainty-Adjusted ROP

Visualization: Plotly (Dynamic Risk Distributions & Forecast Overlays)
