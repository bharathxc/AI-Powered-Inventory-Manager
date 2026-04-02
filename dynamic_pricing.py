import pandas as pd

def suggest_dynamic_price(item_title, current_stock, reorder_point, original_price, forecast_trend, threshold=0.10):
    avg_future_demand = forecast_trend['yhat'].tail(4).mean()
    avg_historic_demand = forecast_trend['yhat'].mean()
    demand_multiplier = avg_future_demand / avg_historic_demand if avg_historic_demand > 0 else 1
    
    # Use the threshold from the slider (e.g., 0.05 for Aggressive)
    upper_bound = 1 + threshold
    lower_bound = 1 - threshold

    if current_stock <= reorder_point and demand_multiplier > upper_bound:
        recommended_price = original_price * 1.15
        reason = f"🚀 Scarcity Surge: Demand up >{int(threshold*100)}% while stock is low."
    elif current_stock > (reorder_point * 1.5) and demand_multiplier < lower_bound:
        recommended_price = original_price * 0.85
        reason = f"📢 Clearance: Demand down >{int(threshold*100)}% with high surplus."
    else:
        recommended_price = original_price
        reason = "✅ Market Stable: Volatility is within current sensitivity limits."
        
    return round(recommended_price, 2), reason