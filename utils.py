import tempfile
from fpdf import FPDF
import pandas as pd
import re

def clean_unicode(text):
    # Removes emojis and characters outside Latin-1 range
    return text.encode('latin-1', 'ignore').decode('latin-1')

def download_pdf(df: pd.DataFrame, summary: list) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Wealth Analyzer Report", ln=True, align="C")
    pdf.ln(10)

    # Table Headers
    pdf.set_font("Arial", "B", 10)
    headers = df.columns.tolist()
    for header in headers:
        pdf.cell(40, 10, txt=clean_unicode(str(header)), border=1)
    pdf.ln()

    # Table Data
    pdf.set_font("Arial", "", 10)
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, txt=clean_unicode(str(item)), border=1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Insights & Risks", ln=True)

    pdf.set_font("Arial", "", 10)
    for line in summary:
        clean_line = clean_unicode("• " + str(line))
        pdf.multi_cell(0, 10, txt=clean_line)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        tmpfile.seek(0)
        return tmpfile.read()
import io

def get_excel_template():
    sample_data = pd.DataFrame({
        "Asset Name": ["HDFC Bank", "Bitcoin"],
        "Type": ["Equity", "Crypto"],
        "Purchase Value": [100000, 30000],
        "Current Value": [125000, 55000],
        "Purchase Date": ["2021-01-01", "2020-11-15"]
    })

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sample_data.to_excel(writer, index=False, sheet_name="Portfolio")

    output.seek(0)
    return output.read()

