# Redefine scenarios to include different caps
caps = [10_000_000, 25_000_000, 50_000_000]
discounts = [0.0, 0.2, 0.4, 0.5]
initial_investment = 100_000

# Generate data for combinations of discounts and caps
rows = []
for cap in caps:
    for discount in discounts:
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
                "Cap": f"{int(cap/1e6)}M",
                "Discount": f"{int(discount*100)}%"
            })

df = pd.DataFrame(rows)

# Create subplots with rows for each metric
fig = make_subplots(rows=4, cols=1,
                    subplot_titles=["Valution YOU get (low=good)", "Equity", "Value of your equity", "ROI"],
                    shared_xaxes=True)

# Mapping of rows to the metrics
metrics = ["Convert_at", "Equity", "Value_of_Equity", "ROI"]
metric_labels = ["Conversion Valuation", "Equity (%)", "Value of Equity", "ROI (x)"]

# Add traces for each metric, differentiated by cap
for row, (metric, label) in enumerate(zip(metrics, metric_labels), start=1):
    for cap in caps:
        for discount in discounts:
            filtered_df = df[(df["Cap"] == f"{int(cap/1e6)}M") & (df["Discount"] == f"{int(discount*100)}%")]
            fig.add_trace(
                go.Scatter(x=filtered_df["Valuation"], y=filtered_df[metric] * (100 if metric == "Equity" else 1),
                           mode='lines', name=f"Cap: {int(cap/1e6)}M, Discount: {int(discount*100)}%"),
                row=row, col=1
            )

# Update layout
fig.update_layout(height=2000, width=800, title_text="Investment Metrics across Different Caps and Discounts")
fig.update_xaxes(title_text="Valuation ($)")
fig.update_yaxes(title_text="Value", tickformat=".0%")
fig.show()
