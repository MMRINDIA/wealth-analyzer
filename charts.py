# analyzer/charts.py

import matplotlib.pyplot as plt
import streamlit as st

def generate_pie_chart(df, output_path="outputs/portfolio_pie.png", mode="cli"):
    grouped = df.groupby("Type")["Current Value"].sum()
    colors = plt.cm.Set3.colors[:len(grouped)]

    plt.figure(figsize=(8, 8))
    plt.pie(
        grouped,
        labels=grouped.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors
    )
    plt.title("Portfolio Allocation", fontsize=16)
    plt.axis('equal')
    plt.tight_layout()

    if mode == "streamlit":
        st.pyplot(plt.gcf())
    else:
        plt.savefig(output_path)
        print(f"📊 Pie chart saved to: {output_path}")
        plt.show()

    plt.close()
