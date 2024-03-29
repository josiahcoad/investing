import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define scenarios
scenarios = [
    {"cap": 10_000_000, "discount": 0.0, "initial_investment": 100_000},
    {"cap": 25_000_000, "discount": 0.25, "initial_investment": 100_000},
    {"cap": 50_000_000, "discount": 0.50, "initial_investment": 100_000}
]

# Generate data
rows = []
for scenario in scenarios:
    cap = scenario["cap"]
    discount = scenario["discount"]
    initial_investment = scenario["initial_investment"]
    
    for valuation in np.arange(5_000_000, 100_000_000, 10_000):
        convert_at = min(valuation * (1 - discount), cap)
        equity = initial_investment / convert_at
        value_of_equity = equity * valuation
        roi = value_of_equity / initial_investment
        
        rows.append({
            "Valuation": valuation,
            "Convert_at": convert_at,
            "Equity": equity,
            "Value_of_Equity": value_of_equity,
            "ROI": roi,
            "Scenario": f"{int(discount*100)}% discount, {int(cap/1e6)}M cap"
        })

df = pd.DataFrame(rows)

# Create subplots
fig = make_subplots(rows=4, cols=1, subplot_titles=("Valution YOU get (low=good)", "Equity", "Value of your equity", "ROI"))

# Add traces
for scenario in df["Scenario"].unique():
    scenario_df = df[df["Scenario"] == scenario]
    
    # Valuation YOU get (low=good)
    fig.add_trace(go.Scatter(x=scenario_df["Valuation"], y=scenario_df["Convert_at"], mode='lines', name=scenario), row=1, col=1)
    
    # Equity
    fig.add_trace(go.Scatter(x=scenario_df["Valuation"], y=scenario_df["Equity"] * 100, mode='lines', name=scenario), row=2, col=1)
    
    # Value of your equity
    fig.add_trace(go.Scatter(x=scenario_df["Valuation"], y=scenario_df["Value_of_Equity"], mode='lines', name=scenario), row=3, col=1)
    
    # ROI
    fig.add_trace(go.Scatter(x=scenario_df["Valuation"], y=scenario_df["ROI"], mode='lines', name=scenario), row=4, col=1)

# Update layout
fig.update_layout(height=1200, width=600, title_text="Value of a $100k investment")
fig.update_xaxes(title_text="Valuation at time of priced round ($M)", row=4, col=1)
fig.show()
