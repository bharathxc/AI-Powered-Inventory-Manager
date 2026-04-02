import pandas as pd
import numpy as np
from pathlib import Path

def generate_realistic_demand(input_csv='data/raw_data.csv', output_csv='data/demand_data.csv'):
    raw_df = pd.read_csv(input_csv)
    weeks = pd.date_range('2024-01-01', periods=52, freq='W')

    simulated = []
    for _, row in raw_df.iterrows():
        # Mix of high-volume and low-volume products
        base_demand = np.random.choice([5, 15, 40]) 
        
        # Randomly assign a trend: Growing, Shrinking, or Volatile
        trend_slope = np.random.uniform(-0.5, 0.5)
        
        for i, week in enumerate(weeks):
            # Seasonality + Trend + Random Noise
            seasonality = 10 * np.sin(2 * np.pi * i / 52)
            noise = np.random.poisson(lam=5)
            
            demand = max(0, int(base_demand + (i * trend_slope) + seasonality + noise))
            
            simulated.append({
                'title': row['title'],
                'week': week,
                'demand': demand
            })

    df = pd.DataFrame(simulated)
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print("New varied demand data generated.")

if __name__ == '__main__':
    generate_realistic_demand()