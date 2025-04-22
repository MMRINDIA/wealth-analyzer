# analyzer/sip_projection.py

def run_sip_projection(monthly_investment, years, annual_return=0.12):
    summary = []
    months = years * 12
    total_invested = monthly_investment * months

    # Future value of SIP formula
    r = annual_return / 12  # Monthly return
    future_value = monthly_investment * (((1 + r) ** months - 1) * (1 + r)) / r

    gain = future_value - total_invested

    summary.append(f"Total Invested: ₹{total_invested:,.0f}")
    summary.append(f"Future Value: ₹{future_value:,.0f}")
    summary.append(f"Estimated Gain: ₹{gain:,.0f}")

    return summary
