import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.metric-container {
    background-color: #1E222A;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
data = pd.read_csv("dataset/sales_data_project_dataset.csv")

# Fix date format
data['order_date'] = pd.to_datetime(data['order_date'], format="mixed", dayfirst=True)

# Fix sales column
data['sales'] = data['sales'].astype(str).str.replace(',', '')
data['sales'] = pd.to_numeric(data['sales'], errors='coerce')

# Sidebar filters
st.sidebar.title("📌 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    data["region"].unique(),
    default=data["region"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [data['order_date'].min(), data['order_date'].max()]
)

# Filter dataset
filtered = data[
    (data["region"].isin(regions)) &
    (data["order_date"] >= pd.to_datetime(date_range[0])) &
    (data["order_date"] <= pd.to_datetime(date_range[1]))
]

# KPI calculations
total_sales = filtered["sales"].sum()
total_orders = filtered.shape[0]
avg_sales = filtered["sales"].mean()
products = filtered["product_name"].nunique()

# Title
st.title("📊 Sales Analytics Dashboard")

# KPI row
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("📊 Average Sales", f"${avg_sales:,.2f}")
col4.metric("🛒 Products", products)

st.markdown("---")

# Charts row
col5, col6 = st.columns(2)

# Sales by region
region_sales = filtered.groupby("region")["sales"].sum().reset_index()

fig1 = px.bar(
    region_sales,
    x="region",
    y="sales",
    color="region",
    title="Sales by Region",
    template="plotly_dark"
)

col5.plotly_chart(fig1, use_container_width=True)

# Top products
top_products = (
    filtered.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    title="Top Selling Products",
    template="plotly_dark"
)

col6.plotly_chart(fig2, use_container_width=True)

# Monthly sales trend
st.subheader("📈 Monthly Sales Trend")

filtered["month"] = filtered["order_date"].dt.to_period("M").astype(str)

monthly_sales = filtered.groupby("month")["sales"].sum().reset_index()

fig3 = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# Data table
st.subheader("📄 Dataset Preview")

st.dataframe(filtered.head(100))
