import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ASBI Dashboard", layout="wide")
st.title("📊 Gutty Wave Runner - Financial Dashboard")

# KPIs
total_revenue = 6_086_420.05
net_profit = 4_339_726.16
cash_end = 7_954_839.88
total_receivables = 2_205_573.10

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"Rs {total_revenue:,.2f}")
kpi2.metric("📈 Net Profit", f"Rs {net_profit:,.2f}")
kpi3.metric("💵 Cash Balance", f"Rs {cash_end:,.2f}")
kpi4.metric("📉 Total Receivables", f"Rs {total_receivables:,.2f}")

# Top customers overdue
top_customers_data = {
    'Customer': [
        "Coral Garden Ltd", "Eric'Seduction", "Lynn and Sea Co Ltd",
        "Mr. Genaro Bhuttoo", "Mr. Jean Eric"
    ],
    'Amount Due': [
        2_205_573.10, 1_200_197.50, 1_526_108.65, 83_100.00, 81_803.45
    ]
}
df_top = pd.DataFrame(top_customers_data)

st.subheader("📌 Top 5 Overdue Customers")
st.dataframe(df_top.style.format({"Amount Due": "Rs {:,.2f}"}))

fig = px.bar(df_top, x='Customer', y='Amount Due',
             text='Amount Due', title="Top Overdue Customers",
             labels={'Amount Due': 'Rs'}, height=400)

fig.update_traces(texttemplate='Rs %{text:,.0f}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=True)
