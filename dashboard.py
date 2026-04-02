import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from forecasting import forecast_demand
from inventory_optimizer import calculate_reorder_and_safety_stock, get_current_stock
from dynamic_pricing import suggest_dynamic_price
from simulation_engine import run_stockout_simulation
from negotiation_agent import draft_negotiation_email

# --- Page Configuration ---
st.set_page_config(page_title="Tech-Aura AI Engine", layout="wide", page_icon="🔌")
st.title("🔌 Tech-Aura: Advanced AI Inventory Engine")
st.markdown("---")

# --- 1. Load Master Tech Data ---
@st.cache_data
def load_master_data():
    try:
        return pd.read_csv('tech_inventory_master.csv')
    except FileNotFoundError:
        st.error("Missing 'tech_inventory_master.csv'. Please run the data generator first.")
        return pd.DataFrame()

master_df = load_master_data()

if not master_df.empty:
    # --- Sidebar: Global AI Strategy ---
    st.sidebar.header("📡 Strategy Controller")
    st.sidebar.info("Adjusting these recalibrates the Bayesian safety buffers in real-time.")
    
    sim_service_level = st.sidebar.select_slider(
        "Desired Service Level", 
        options=[0.80, 0.90, 0.95, 0.99], 
        value=0.95,
        help="Higher service levels increase safety stock to prevent stockouts."
    )
    
    # Statistical Z-Mapping
    service_map = {0.80: 1.28, 0.90: 1.65, 0.95: 1.96, 0.99: 2.58}
    z_score = service_map[sim_service_level]

    # --- 2. Product Selection ---
    product_options = master_df['product_id'] + " - " + master_df['title']
    selected_option = st.selectbox("Search Product SKU / Title:", product_options)
    selected_id = selected_option.split(" - ")[0]
    
    # Fetch Metadata
    product_info = master_df[master_df['product_id'] == selected_id].iloc[0]

    # --- 3. Backend Execution ---
    with st.spinner(f"Analyzing {selected_id} via Prophet..."):
        # Run Forecast
        results = forecast_demand(selected_id)
        forecast = results['forecast']
        model = results['model']
        
        # Run Optimization & Risk Audit
        opt = calculate_reorder_and_safety_stock(results, lead_time=int(product_info['lead_time_weeks']), service_factor=z_score)
        curr_stock = get_current_stock(selected_id)
        
        # Run Monte Carlo Simulation
        sim_results = run_stockout_simulation(curr_stock, forecast.iloc[-1], int(product_info['lead_time_weeks']))

    # --- 4. High-Level Metrics Row ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Current Stock", f"{curr_stock} units")
    with m2:
        st.metric("AI Reorder Point", f"{opt['Reorder Point']} units", 
                  delta=int(curr_stock - opt['Reorder Point']), delta_color="inverse")
    with m3:
        st.metric("Model Health (MAPE)", f"{opt['Forecast Error (MAPE)']}%", help="Lower is better.")
    with m4:
        st.metric("Stockout Risk", f"{sim_results['stockout_probability']}%", 
                  delta=sim_results['risk_score'], delta_color="off")

    # --- 5. Navigation Tabs ---
    tab1, tab2, tab3 = st.tabs(["📈 Predictive Analytics", "⚖️ Risk & Simulation", "🤖 Autonomous Agent"])

    with tab1:
        st.subheader("Time-Series Demand Forecast")
        
        # Main Forecast Plot with Bayesian Uncertainty
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['y'], name="Actual Sales", mode='markers'))
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name="AI Prediction", line=dict(color='deepskyblue', width=3)))
        
        # Shaded Uncertainty Interval
        fig.add_trace(go.Scatter(
            x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
            y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
            fill='toself', fillcolor='rgba(0,176,246,0.15)', line=dict(color='rgba(255,255,255,0)'),
            name="Uncertainty Range"
        ))
        
        fig.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 View Model Decomposition (Explainable AI)"):
            from prophet.plot import plot_components_plotly
            comp_fig = plot_components_plotly(model, forecast)
            st.plotly_chart(comp_fig, use_container_width=True)

    with tab2:
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("Monte Carlo Risk Distribution")
            hist_data = [sim_results['sim_data']]
            fig_sim = ff.create_distplot(hist_data, ['Probable Demand'], bin_size=2, show_hist=False, colors=['#00B0F6'])
            fig_sim.add_vline(x=curr_stock, line_dash="dash", line_color="red", annotation_text="Current Stock")
            fig_sim.update_layout(showlegend=False, height=350, margin=dict(t=20))
            st.plotly_chart(fig_sim, use_container_width=True)
            
        with col_right:
            st.subheader("Inventory Financials")
            # Logic from dynamic_pricing.py
            new_price, reason = suggest_dynamic_price(
                product_info['title'], curr_stock, opt['Reorder Point'], 
                product_info['base_price'], forecast
            )
            
            st.write(f"**Unit Cost:** ${product_info['unit_cost']}")
            st.write(f"**Market Price:** ${product_info['base_price']}")
            st.write(f"**AI Suggested Price:** `${new_price}`")
            st.info(f"**Pricing Reason:** {reason}")

    with tab3:
        st.subheader("Strategic Procurement Agent")
        if curr_stock <= opt['Reorder Point']:
            shortfall = opt['Reorder Point'] - curr_stock
            rev_at_risk = round(shortfall * product_info['base_price'], 2)
            
            st.warning(f"Shortfall detected: {shortfall} units. ${rev_at_risk} in revenue is currently at risk.")
            
            email_body = draft_negotiation_email(
                product_info['title'], shortfall, rev_at_risk, product_info['base_price']
            )
            
            final_email = st.text_area("Review Agent Negotiation Draft", email_body, height=250)
            target_vendor = st.text_input("Vendor Address", product_info['vendor_email'])
            
            if st.button("🚀 Dispatch to Vendor"):
                st.success("Negotiation dispatched via SMTP successfully.")
        else:
            st.success("Current stock levels satisfy the safety buffer. No agent action required.")

else:
    st.warning("Please ensure 'tech_inventory_master.csv' is in the root directory to begin.")