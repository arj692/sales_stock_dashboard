import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Read your Excel data (no more 'Downloads/' here!)
sales_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Sales_Data')
inventory_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Inventory_Data')

st.title("📊 Multi-Product Sales & Stock Dashboard")

# Dropdown to select month
month = st.selectbox("Select Month", sales_df['Month'].unique())

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
    lambda row: 'Restock Needed' if row['Current Stock'] < row['Reorder Level'] else 'Stock OK',
    axis=1
)

# Show data
st.write("### Sales & Stock Summary for", month)
st.dataframe(combined_summary)

# Dynamic bar colors
bar_colors = ['red' if sales > stock else 'green' 
              for sales, stock in zip(combined_summary['Units Sold'], combined_summary['Current Stock'])]

# Plotly Chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=combined_summary['Product'],
    y=combined_summary['Units Sold'],
    name='Units Sold',
    marker_color=bar_colors
))

fig.add_trace(go.Scatter(
    x=combined_summary['Product'],
    y=combined_summary['Current Stock'],
    name='Current Stock',
    mode='lines+markers',
    line=dict(color='orange', dash='dash')
))

fig.update_layout(
    title=f'Units Sold vs Current Stock ({month})',
    xaxis_title='Product',
    yaxis_title='Units',
    template='plotly_white'
)

st.plotly_chart(fig)
