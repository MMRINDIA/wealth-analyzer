# analyzer/ai_summary.py

def generate_ai_summary(df):
    summary = []

    equity = df[df["Type"].isin(["Equity", "Mutual Fund"])]["Current Value"].sum()
    debt = df[df["Type"] == "Debt"]["Current Value"].sum()
    crypto = df[df["Type"] == "Crypto"]["Current Value"].sum()
    total = df["Current Value"].sum()

    equity_pct = (equity / total) * 100 if total else 0
    debt_pct = (debt / total) * 100 if total else 0
    crypto_pct = (crypto / total) * 100 if total else 0

    if equity_pct > 60:
        summary.append("📌 Your portfolio is equity-heavy. Consider balancing with debt or gold.")
    elif debt_pct > 40:
        summary.append("📌 Strong debt foundation. You could add equity for higher long-term growth.")
    elif crypto_pct > 20:
        summary.append("📌 High crypto exposure. Be cautious of volatility.")

    summary.append("🧠 Tip: Rebalancing every 6 months helps maintain healthy diversification.")

    return summary
