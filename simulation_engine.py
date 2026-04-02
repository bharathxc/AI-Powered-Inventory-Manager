import numpy as np
import pandas as pd

def run_stockout_simulation(current_stock, forecast_row, lead_time_weeks, iterations=1000):
    """
    Advanced Monte Carlo Simulation:
    Generates 1000 possible demand scenarios for the lead time period
    to calculate the mathematical probability of running out of stock.
    """
    # Use the model's uncertainty to define the 'width' of our random scenarios
    # yhat_upper - yhat_lower represents the 95% confidence interval
    uncertainty_range = forecast_row['yhat_upper'] - forecast_row['yhat_lower']
    sigma = uncertainty_range / 3.92  # Derived from Z-distribution for 95%
    
    expected_demand = forecast_row['yhat'] * lead_time_weeks
    
    # Generate 1000 random futures based on a Normal Distribution
    simulated_demands = np.random.normal(expected_demand, sigma * np.sqrt(lead_time_weeks), iterations)
    
    # Calculate how many times demand exceeds our current stock
    stockouts = np.sum(simulated_demands > current_stock)
    stockout_prob = (stockouts / iterations) * 100
    
    return {
        'stockout_probability': round(stockout_prob, 2),
        'sim_data': simulated_demands,
        'risk_score': "CRITICAL" if stockout_prob > 20 else "STABLE"
    }