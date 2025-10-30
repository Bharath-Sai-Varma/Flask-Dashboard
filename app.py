from flask import Flask, render_template, send_file
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__)

# Load Excel
df = pd.read_excel("sample_sales.xlsx")

@app.route("/")
def dashboard():
    # --- Chart 1: Sales by Category ---
    fig1 = px.bar(df.groupby("Category", as_index=False)["Sales"].sum(),
                  x="Category", y="Sales", color="Category",
                  title="Total Sales by Category")
    fig1.update_layout(template="plotly_dark")

    # --- Chart 2: Sales by Region ---
    fig2 = px.pie(df, names="Region", values="Sales",
                  title="Sales Distribution by Region",
                  color_discrete_sequence=px.colors.sequential.RdBu)

    # Convert plots to HTML
    graph1 = pio.to_html(fig1, full_html=False)
    graph2 = pio.to_html(fig2, full_html=False)

    return render_template("index.html", graph1=graph1, graph2=graph2)

@app.route("/download")
def download_excel():
    path = "sample_sales.xlsx"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
