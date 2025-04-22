# analyzer/pdf_export.py

from fpdf import FPDF
import os
from datetime import datetime

class PDFExporter(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Wealth Analyzer - Portfolio Report", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(5)

    def add_portfolio_table(self, df):
        self.set_font("Arial", "B", 10)
        col_widths = [40, 30, 30, 30, 30]

        headers = ["Asset Name", "Type", "Purchase Value", "Current Value", "Purchase Date"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1)
        self.ln()

        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            self.cell(col_widths[0], 10, str(row["Asset Name"]), border=1)
            self.cell(col_widths[1], 10, str(row["Type"]), border=1)
            self.cell(col_widths[2], 10, f'₹{int(row["Purchase Value"]):,}', border=1)
            self.cell(col_widths[3], 10, f'₹{int(row["Current Value"]):,}', border=1)
            self.cell(col_widths[4], 10, str(row["Purchase Date"]), border=1)
            self.ln()

    def add_summary(self, lines):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Summary:", ln=True)
        self.set_font("Arial", "", 10)
        for line in lines:
            self.multi_cell(0, 10, line)

def generate_pdf(df, summary, filename="portfolio_report.pdf"):
    pdf = PDFExporter()
    pdf.add_page()
    pdf.add_portfolio_table(df)
    pdf.add_summary(summary)

    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)
    pdf.output(path)
    return path
