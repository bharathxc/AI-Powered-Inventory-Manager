import pandas as pd
import numpy as np
from forecasting import forecast_demand
from inventory_optimizer import calculate_reorder_and_safety_stock, get_current_stock

def generate_global_risk_report(items, lead_time, service_factor):
    """Calculates risk metrics for the entire inventory at once."""
    report_list = []
    
    # In a real app, you'd load prices from scrapper.py output here
    try:
        prices_df = pd.read_csv('data/raw_data.csv')[['title', 'price']]
    except:
        prices_df = pd.DataFrame()

    for item in items[:20]: # Process top 20 for speed
        try:
            forecast = forecast_demand(item)
            opt_results = calculate_reorder_and_safety_stock(forecast, lead_time, service_factor)
            current_stock = get_current_stock(item)
            
            # Financial Impact Logic
            price = prices_df[prices_df['title'] == item]['price'].values[0] if not prices_df.empty else 10.0
            
            avg_demand = forecast['yhat'].mean()
            stockout_risk = "High" if current_stock <= opt_results['Reorder Point'] else "Low"
            
            report_list.append({
                "Product": item,
                "Current Stock": current_stock,
                "Reorder Point": opt_results['Reorder Point'],
                "Risk Level": stockout_risk,
                "Potential Revenue Loss": round(max(0, opt_results['Reorder Point'] - current_stock) * price, 2)
            })
        except Exception as e:
            continue
            
    return pd.DataFrame(report_list)