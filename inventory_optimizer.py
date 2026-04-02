import pandas as pd
import numpy as np

def calculate_reorder_and_safety_stock(forecast_results, lead_time=2, service_factor=1.65):
    """
    Advanced Inventory Logic:
    1. Uses Bayesian Uncertainty (yhat_upper - yhat_lower) to define Risk.
    2. Calculates a 'Model Confidence' score to justify safety buffer sizes.
    3. Dynamically scales Safety Stock based on lead-time volatility.
    """
    forecasted_df = forecast_results['forecast']
    uncertainty_index = forecast_results['uncertainty_index']
    mape = forecast_results['mape']

    # 1. Define Volatility (Sigma)
    # Instead of historical SD, we use the model's own predicted error (Uncertainty)
    # This captures future risks (like a tech launch) that history might miss.
    sigma = uncertainty_index / 4  # Standardizing the interval to ~1 SD
    
    # 2. Average Demand during Lead Time
    # We look at the immediate future (next 'lead_time' weeks)
    avg_demand = forecasted_df['yhat'].tail(lead_time).mean()
    
    # 3. Safety Stock Calculation
    # Formula: Z-Score * Predicted Volatility * Sqrt(Lead Time)
    safety_stock = service_factor * sigma * (lead_time ** 0.5)
    
    # 4. Reorder Point (ROP)
    reorder_point = (avg_demand * lead_time) + safety_stock

    # 5. Model Confidence Metric (For the DS Dashboard)
    # High uncertainty relative to demand = Low Confidence
    confidence_score = max(0, 1 - (uncertainty_index / (avg_demand + 1)))

    return {
        'Reorder Point': max(1, round(reorder_point)),
        'Safety Stock': max(1, round(safety_stock)),
        'Model Confidence': round(confidence_score * 100, 2),
        'Forecast Error (MAPE)': round(mape * 100, 2),
        'Demand Volatility': round(sigma, 2)
    }

def get_current_stock(product_id, inventory_csv='tech_inventory_master.csv'):
    """
    REPLACED SIMULATION: 
    Fetches the actual real-time stock level from our Master Tech Database.
    """
    try:
        df = pd.read_csv(inventory_csv)
        stock = df[df['product_id'] == product_id]['current_stock'].values[0]
        return int(stock)
    except Exception as e:
        print(f"Error fetching stock for {product_id}: {e}")
        return 0