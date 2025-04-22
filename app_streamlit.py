import streamlit as st
import pandas as pd
from analyzer.engine import analyze_portfolio
from analyzer.charts import generate_pie_chart
from analyzer.sip_projection import run_sip_projection
from analyzer.utils import get_excel_template  # ✅ Only using get_excel_template

st.set_page_config(page_title="Wealth Analyzer", layout="wide")
st.sidebar.image("static/logo.png", use_container_width=True)
page = st.sidebar.radio("📂 Navigate", ["📊 Portfolio Analysis", "📈 SIP Simulation", "📬 Contact Us"])
st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ for mindful investors")

df = pd.DataFrame()

if page == "📊 Portfolio Analysis":
    st.title("💰 Wealth Analyzer")

    # Upload Option
    uploaded_file = st.file_uploader("📥 Upload your portfolio (.xlsx)", type=["xlsx"])
    st.download_button(
        "⬇️ Download Sample Excel Format",
        data=get_excel_template(),
        file_name="sample_portfolio.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Manual Inputs
    st.markdown("Or manually enter up to 2 investments:")
    manual_entries = []
    for i in range(1, 3):
        with st.expander(f"Manual Entry {i}"):
            asset = st.text_input(f"Asset Name {i}", key=f"name_{i}")
            type_ = st.selectbox(f"Type {i}", ["Equity", "Mutual Fund", "Crypto", "Debt", "Gold", "Cash"], key=f"type_{i}")
            purchase = st.number_input(f"Purchase Value ₹ {i}", min_value=0, value=0, step=1000, key=f"purchase_{i}")
            current = st.number_input(f"Current Value ₹ {i}", min_value=0, value=0, step=1000, key=f"current_{i}")
            date = st.date_input(f"Purchase Date {i}", key=f"date_{i}")
            if asset and purchase and current:
                manual_entries.append({
                    "Asset Name": asset,
                    "Type": type_,
                    "Purchase Value": purchase,
                    "Current Value": current,
                    "Purchase Date": pd.to_datetime(date)
                })

    df_manual = pd.DataFrame(manual_entries)

    if uploaded_file:
        df_uploaded = pd.read_excel(uploaded_file)
        df = pd.concat([df_uploaded, df_manual], ignore_index=True)
    else:
        df = df_manual

    # Show Portfolio
    if not df.empty:
        st.success("✅ Portfolio loaded successfully.")
        st.subheader("📋 Portfolio Table")
        df["Purchase Date"] = df["Purchase Date"].astype(str)
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Insights & Risks")
        report = analyze_portfolio(df)
        for line in report["summary"]:
            st.write("•", line)

        st.subheader("📈 Portfolio Allocation")
        generate_pie_chart(df, mode="streamlit")

elif page == "📈 SIP Simulation":
    st.title("📈 SIP Projection Tool")
    monthly = st.number_input("💸 Monthly Investment (₹)", min_value=1000, value=10000)
    years = st.slider("🗓️ Investment Duration (Years)", 1, 30, 10)

    if st.button("🔍 Simulate SIP"):
        summary = run_sip_projection(monthly, years)
        for line in summary:
            st.write("•", line)

elif page == "📬 Contact Us":
    st.title("📬 Contact & Feedback")
    st.write("Reach us at: support@wealthanalyzer.ai")
