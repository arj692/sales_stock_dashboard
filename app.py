import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from xhtml2pdf import pisa
import base64

# Set page config
st.set_page_config(page_title="ASBI Sales & Stock Dashboard", layout="wide")

# Load data
sales_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Sales_Data')
inventory_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Inventory_Data')

# Sidebar navigation
st.sidebar.title("📊 ASBI Dashboard")
page = st.sidebar.radio("Go to", ["Dashboard", "Trends & Forecast", "Download Reports"])

# Filters
month_filter = st.sidebar.selectbox("Select Month", sales_df['Month'].unique())
product_filter = st.sidebar.multiselect(
    "Select Product(s)",
    options=sales_df[sales_df['Month'] == month_filter]['Product'].unique(),
    default=list(sales_df[sales_df['Month'] == month_filter]['Product'].unique())
)

filtered_sales = sales_df[
    (sales_df['Month'] == month_filter) &
    (sales_df['Product'].isin(product_filter))
]
summary = filtered_sales.groupby('Product').agg({
    'Units Sold': 'sum',
    'Total Sales': 'sum'
}).reset_index()
summary = pd.merge(summary, inventory_df, on='Product', how='left')
summary['Stock Status'] = summary.apply(
    lambda row: '🔴 Restock Needed' if row['Current Stock'] < row['Reorder Level'] else '🟢 Stock OK',
    axis=1
)
summary['% Stock Remaining'] = round(
    (summary['Current Stock'] / (summary['Current Stock'] + summary['Units Sold'])) * 100, 1
)

# Dashboard Page
if page == "Dashboard":
    st.title("📌 KPI Overview")
    k1, k2, k3 = st.columns(3)
    k1.metric("Units Sold", f"{summary['Units Sold'].sum()}")
    k2.metric("Total Sales", f"${summary['Total Sales'].sum():,.2f}")
    k3.metric("Restock Alerts", f"{summary['Stock Status'].str.contains('Restock').sum()}")

    st.subheader("📋 Sales & Stock Summary")
    st.dataframe(summary)

    fig = go.Figure(data=[
        go.Bar(name='Units Sold', x=summary['Product'], y=summary['Units Sold']),
        go.Bar(name='Current Stock', x=summary['Product'], y=summary['Current Stock'])
    ])
    fig.update_layout(barmode='group', title="Sales vs Stock")
    st.plotly_chart(fig, use_container_width=True)

# Trends & Forecast Page
elif page == "Trends & Forecast":
    st.title("📈 Trends & Forecast")
    sales_by_month = sales_df[sales_df['Product'].isin(product_filter)].groupby('Month').agg({
        'Units Sold': 'sum',
        'Total Sales': 'sum'
    }).reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=sales_by_month['Month'], y=sales_by_month['Units Sold'], name="Units Sold", mode='lines+markers'))
    fig2.add_trace(go.Scatter(x=sales_by_month['Month'], y=sales_by_month['Total Sales'], name="Total Sales", mode='lines+markers'))

    st.plotly_chart(fig2, use_container_width=True)

    last_month_units = sales_by_month['Units Sold'].iloc[-1]
    forecast = round(last_month_units * 1.1)
    st.info(f"📌 Forecast for next month (Units Sold): **{forecast}** (estimated +10%)")

# Download Reports Page
elif page == "Download Reports":
    st.title("⬇ Download Center")

    # CSV
    csv = summary.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="summary.csv", mime='text/csv')

    # PDF
    def create_pdf(df):
        html = f"""
        <h2>ASBI Sales & Stock Summary</h2>
        <img src="https://via.placeholder.com/150x50.png?text=ASBI+Logo" />
        {df.to_html(index=False)}
        """
        buffer = BytesIO()
        pisa.CreatePDF(html, dest=buffer)
        return buffer

    if st.button("Generate PDF"):
        pdf_file = create_pdf(summary)
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="summary.pdf",
            mime="application/pdf"
        )
