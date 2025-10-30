from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load Excel
df = pd.read_excel("sales_data.xlsx")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    filtered_df = df.copy()

    # Apply filters
    selected_region = request.form.get("region", "All")
    selected_category = request.form.get("category", "All")

    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    # KPIs
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_quantity = filtered_df["Quantity"].sum()

    # Charts
    fig1 = px.bar(filtered_df.groupby("Category", as_index=False)["Sales"].sum(),
                  x="Category", y="Sales", color="Category",
                  title="Total Sales by Category",
                  color_discrete_sequence=px.colors.qualitative.Pastel)

    fig2 = px.pie(filtered_df, names="Region", values="Sales",
                  title="Sales Share by Region",
                  color_discrete_sequence=px.colors.sequential.Tealgrn)

    fig3 = px.line(filtered_df.groupby("Date", as_index=False)["Sales"].sum(),
                   x="Date", y="Sales", title="Sales Trend Over Time",
                   markers=True, color_discrete_sequence=["#00bcd4"])

    graph1 = pio.to_html(fig1, full_html=False)
    graph2 = pio.to_html(fig2, full_html=False)
    graph3 = pio.to_html(fig3, full_html=False)

    regions = ["All"] + sorted(df["Region"].unique().tolist())
    categories = ["All"] + sorted(df["Category"].unique().tolist())

    return render_template(
        "index.html",
        graph1=graph1, graph2=graph2, graph3=graph3,
        regions=regions, categories=categories,
        selected_region=selected_region, selected_category=selected_category,
        total_sales=total_sales, total_profit=total_profit, total_quantity=total_quantity
    )

@app.route("/download")
def download_excel():
    return send_file("sales_data.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
