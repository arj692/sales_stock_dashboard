import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from xhtml2pdf import pisa
import base64

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="📊 Multi-Product Sales & Stock Dashboard", layout="wide")

# ---------------------- STYLE ----------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #F9FAFC;
    }
    .big-font {
        font-size:28px !important;
        color: #2E86C1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- DATA ----------------------
sales_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Sales_Data')
inventory_df = pd.read_excel('sample_sales_inventory.xlsx', sheet_name='Inventory_Data')

st.markdown('<p class="big-font">📊 Multi-Product Sales & Stock Dashboard</p>', unsafe_allow_html=True)

# ---------------------- FILTERS ----------------------
col1, col2 = st.columns(2)

month = col1.selectbox("🗓 Select Month", sales_df['Month'].unique())

available_products = sales_df[sales_df['Month'] == month]['Product'].unique()
products_selected = col2.multiselect("🛒 Select Product(s)", available_products, default=list(available_products))

filtered_sales = sales_df[
    (sales_df['Month'] == month) & 
    (sales_df['Product'].isin(products_selected))
]

product_summary = filtered_sales.groupby('Product').agg({
    'Units Sold': 'sum',
    'Total Sales': 'sum'
}).reset_index()

combined_summary = pd.merge(product_summary, inventory_df, on='Product', how='left')

combined_summary['Stock Status'] = combined_summary.apply(
    lambda row: '🔴 Restock Needed' if row['Current Stock'] < row['Reorder Level'] else '🟢 Stock OK',
    axis=1
)

combined_summary['% Stock Remaining'] = round(
    (combined_summary['Current Stock'] / (combined_summary['Units Sold'] + combined_summary['Current Stock'])) * 100, 1
)

# ---------------------- KPIs ----------------------
total_units = combined_summary['Units Sold'].sum()
total_sales = combined_summary['Total Sales'].sum()
restock_count = combined_summary['Stock Status'].str.contains('Restock').sum()

st.subheader("📌 Key Performance Indicators (KPIs)")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Units Sold", f"{total_units}")
kpi2.metric("Total Sales", f"${total_sales:,.2f}")
kpi3.metric("Products Needing Restock", f"{restock_count}")

# ---------------------- DATA TABLE ----------------------
st.subheader("📝 Sales & Inventory Summary")

def color_stock(val):
    color = 'red' if 'Restock' in val else 'green'
    return f'color: {color}'

styled_df = combined_summary.style.applymap(color_stock, subset=['Stock Status'])

# Hide index column
st.dataframe(styled_df.hide(axis="index"))

# ---------------------- CHART ----------------------
fig = go.Figure(data=[
    go.Bar(name='Units Sold', x=combined_summary['Product'], y=combined_summary['Units Sold']),
    go.Bar(name='Current Stock', x=combined_summary['Product'], y=combined_summary['Current Stock'])
])

fig.update_layout(barmode='group', title="Units Sold vs Current Stock")
st.plotly_chart(fig, use_container_width=True)

# ---------------------- CSV EXPORT ----------------------
st.subheader("📥 Download Report")

csv = combined_summary.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name=f'sales_stock_summary_{month}.csv',
    mime='text/csv',
)

# ---------------------- PDF EXPORT ----------------------
def create_pdf(df):
    html = df.to_html(index=False)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    return result if not pisa_status.err else None

if st.button("⬇ Download PDF"):
    pdf_file = create_pdf(combined_summary)
    if pdf_file:
        st.download_button(
            label="Click here to download PDF",
            data=pdf_file,
            file_name=f'sales_stock_summary_{month}.pdf',
            mime='application/pdf'
        )
    else:
        st.error("Error generating PDF.")

