
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AnalyzeWealthAI", layout="centered")

st.title("📊 AnalyzeWealthAI – Portfolio Analyzer")

st.markdown("Upload your **portfolio Excel file** to analyze performance and visualize your investments.")

uploaded_file = st.file_uploader("Upload your .xlsx file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Expecting columns: Asset Name, Type, Purchase Value, Current Value
        df['Gain/Loss'] = df['Current Value'] - df['Purchase Value']
        st.subheader("📋 Portfolio Overview")
        st.dataframe(df)

        st.subheader("📈 Portfolio Distribution")
        fig, ax = plt.subplots()
        asset_names = df['Asset Name']
        values = df['Current Value']
        ax.pie(values, labels=asset_names, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

        st.download_button("📥 Download Gain/Loss Report", data=df.to_csv(index=False), file_name="portfolio_report.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# SIP Calculator
st.markdown("---")
st.header("📆 SIP Calculator")
sip_amt = st.number_input("Monthly SIP Amount (₹)", min_value=100.0, step=100.0)
sip_years = st.slider("Investment Duration (Years)", 1, 30, 10)
sip_return = st.slider("Expected Annual Return (%)", 5, 20, 12)

if st.button("Calculate SIP"):
    r = sip_return / 100 / 12
    n = sip_years * 12
    fv = sip_amt * (((1 + r)**n - 1) * (1 + r) / r)
    invested = sip_amt * n
    gain = fv - invested
    st.success(f"Invested: ₹{int(invested):,}")
    st.info(f"Estimated Final Corpus: ₹{int(fv):,}")
    st.warning(f"Total Gains: ₹{int(gain):,}")
