# analyzer/sip_projection.py

def run_sip_projection(monthly_investment, years, rate_of_return=0.12):
    months = years * 12
    rate = rate_of_return / 12
    future_value = monthly_investment * (((1 + rate)**months - 1) * (1 + rate)) / rate
    total_invested = monthly_investment * months
    gain = future_value - total_invested

    return [
        f"Total Invested: ₹{total_invested:,.0f}",
        f"Future Value: ₹{future_value:,.1f}",
        f"Estimated Gain: ₹{gain:,.0f}"
    ]
