import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="📊 Multi-Product Sales & Stock Dashboard", layout="wide")

# Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #F9FAFC;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Read your Excel data
sales_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Sales_Data')
inventory_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Inventory_Data')

st.title("📊 Multi-Product Sales & Stock Dashboard")

# Dropdown to select month
month = st.selectbox("🗓 Select Month", sales_df['Month'].unique())

# Filter sales data for the selected month
filtered_sales = sales_df[sales_df['Month'] == month]

# Group sales by product
product_summary = filtered_sales.groupby('Product').agg({
    'Units Sold': 'sum',
    'Total Sales': 'sum'
}).reset_index()

# Merge with inventory
combined_summary = pd.merge(product_summary, inventory_df, on='Product', how='left')

# Stock Status column
combined_summary['Stock Status'] = combined_summary.apply(
    lambda row: '🔴 Restock Needed' if row['Current Stock'] < row['Reorder Level'] else '🟢 Stock OK',
    axis=1
)

# Show KPIs
total_units = combined_summary['Units Sold'].sum()
total_sales = combined_summary['Total Sales'].sum()
restock_count = combined_summary['Stock Status'].str.contains('Restock').sum()

st.subheader("📌 Key Performance Indicators (KPIs)")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Units Sold", f"{total_units}")
kpi2.metric("Total Sales", f"${total_sales:,.2f}")
kpi3.metric("Products Needing Restock", f"{restock_count}")

# Show data
st.subheader("📝 Sales & Inventory Summary")
st.dataframe(combined_summary)

# Plot bar chart
fig = go.Figure(data=[
    go.Bar(name='Units Sold', x=combined_summary['Product'], y=combined_summary['Units Sold']),
    go.Bar(name='Current Stock', x=combined_summary['Product'], y=combined_summary['Current Stock'])
])

fig.update_layout(barmode='group', title="Units Sold vs Current Stock")
st.plotly_chart(fig, use_container_width=True)
