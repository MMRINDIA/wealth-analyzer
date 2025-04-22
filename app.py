# app.py

import os
import pandas as pd
import streamlit as st
from analyzer.engine import analyze_portfolio
from analyzer.charts import generate_pie_chart
from analyzer.sip_projection import run_sip_projection

def load_portfolio(file_path="data/sample_portfolio.xlsx"):
    try:
        df = pd.read_excel(file_path)
        st.success("✅ Portfolio loaded successfully.")
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None

def run_cli():
    df = pd.read_excel("data/sample_portfolio.xlsx")
    if df is None: return
    report = analyze_portfolio(df)

    for line in report["summary"]:
        print(line)

    generate_pie_chart(df, mode="cli")

def run_streamlit():
    st.title("💰 Wealth Analyzer – Personal Portfolio Tracker")


    uploaded_file = st.file_uploader("📤 Upload your portfolio Excel file", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded and loaded successfully.")

        # Show analysis
        st.subheader("📊 Portfolio Overview")
        report = analyze_portfolio(df)
        for line in report["summary"]:
            st.write(line)

        st.subheader("📈 Portfolio Allocation")
        generate_pie_chart(df, mode="streamlit")

        # SIP projection
        st.subheader("🧠 SIP Projection (Optional)")
        if st.checkbox("Enable SIP Simulation"):
            monthly = st.number_input("Monthly Investment (₹)", min_value=1000, value=10000)
            years = st.slider("Investment Duration (Years)", 1, 30, 10)
            summary = run_sip_projection(monthly, years)
            for line in summary:
                st.write(line)

if __name__ == "__main__":
    import sys
    if "streamlit" in sys.argv:
        run_streamlit()
    else:
        run_cli()
