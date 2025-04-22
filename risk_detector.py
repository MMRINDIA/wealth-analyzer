# analyzer/risk_detector.py

def detect_risks(df):
    summary_lines = []

    # Asset concentration check
    grouped = df.groupby("Category")["Current Value"].sum()
    total_value = grouped.sum()

    risky = grouped[grouped / total_value > 0.5]
    if not risky.empty:
        summary_lines.append("\n⚠️ Risk Alert: You are highly concentrated in:")
        for cat in risky.index:
            pct = (grouped[cat] / total_value) * 100
            summary_lines.append(f"  - {cat} ({pct:.1f}%)")

    # Debt exposure alert
    if "Debt" in grouped and grouped["Debt"] / total_value < 0.1:
        summary_lines.append("⚠️ Low Debt exposure (<10%). Add some fixed-income for stability.")

    # AI-style suggestion
    summary_lines.append("🧠 Tip: Rebalancing every 6 months helps maintain healthy diversification.")

    return summary_lines
