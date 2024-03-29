import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_data(caps, discounts, initial_investment=100_000):
    rows = []
    for cap in caps:
        for discount in discounts:
            for valuation in np.arange(5_000_000, 100_000_000, 10_000):
                convert_at = np.minimum(valuation * (1 - discount), cap)
                equity = initial_investment / convert_at
                value_of_equity = equity * valuation
                roi = value_of_equity / initial_investment

                rows.append({
                    "Valuation": valuation,
                    "Convert_at": convert_at,
                    "Equity": equity,
                    "Value_of_Equity": value_of_equity,
                    "ROI": roi,
                    "Cap": f"{int(cap/1e6)}M",
                    "Discount": f"{discount*100}%"
                })
    return pd.DataFrame(rows)

def plot_data(df, discounts):
    # Create a subplot for each discount
    cols = len(discounts)
    fig = make_subplots(rows=4, cols=cols, 
                        subplot_titles=[f"Discount: {discount}%" for discount in discounts for _ in range(4)],
                        vertical_spacing=0.1, horizontal_spacing=0.1,
                        shared_xaxes=True, shared_yaxes='rows',
                        specs=[[{'secondary_y': True}] * cols] * 4)
    
    metrics = ["Convert_at", "Equity", "Value_of_Equity", "ROI"]
    metric_labels = ["Valuation YOU get", "Equity", "Value of your equity", "ROI"]

    for col, discount in enumerate(discounts, start=1):
        for row, metric in enumerate(metrics, start=1):
            for cap in df['Cap'].unique():
                filtered_df = df[(df['Discount'] == f"{discount*100}%") & (df['Cap'] == cap)]
                st.write(f"filtered_df[metric]: {filtered_df[metric]}")
                fig.add_trace(go.Scatter(x=filtered_df["Valuation"], 
                                         y=filtered_df[metric] * (100 if metric == "Equity" else 1),
                                         mode='lines', 
                                         name=f"Cap: {cap}"),
                              row=row, col=col, secondary_y=False)

    # Update y-axes titles
    for i, metric_label in enumerate(metric_labels, start=1):
        fig.update_yaxes(title_text=metric_label, row=i, col=1)

    # Update layout
    fig.update_layout(height=1200, width=1000, title_text="Investment Metrics across Different Caps and Discounts")
    return fig

st.title('Investment Metrics Visualizer')

# User inputs for caps and discounts
user_caps = st.text_input('Enter valuation caps separated by commas (e.g., 10M,25M,50M)', '10M,25M,50M')
user_discounts = st.text_input('Enter discounts as percentages separated by commas (e.g., 0%,20%,40%,50%)', '0%,20%,40%,50%')

# Convert inputs to lists of numbers
caps = [float(cap.strip().replace('M', '')) * 1e6 for cap in user_caps.split(',')]
discounts = [float(discount.strip().replace('%', '')) / 100 for discount in user_discounts.split(',')]  # Convert to float for calculations


# Generate and plot data
df = generate_data(caps, discounts)
fig = plot_data(df, discounts)

st.plotly_chart(fig)
