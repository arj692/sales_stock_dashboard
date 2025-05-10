import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ASBI Financial Dashboard", layout="wide")
st.title("📊 Gutty Wave Runner - Financial Dashboard")

# -------------------------------
# KPI VALUES
# -------------------------------
total_revenue = 6_086_420.05
net_profit = 4_339_726.16
cash_end = 7_954_839.88
total_receivables = 2_205_573.10

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"Rs {total_revenue:,.2f}")
kpi2.metric("📈 Net Profit", f"Rs {net_profit:,.2f}")
kpi3.metric("💵 Cash Balance", f"Rs {cash_end:,.2f}")
kpi4.metric("📉 Total Receivables", f"Rs {total_receivables:,.2f}")

# -------------------------------
# Cash Flow Summary
# -------------------------------
st.markdown("---")
st.subheader("💸 Cash Flow Summary")

cash_start = 3_000_000.00
net_cash_movement = 4_954_839.88
cash_end = 7_954_839.88

cf1, cf2, cf3 = st.columns(3)
cf1.metric("Beginning Balance", f"Rs {cash_start:,.2f}")
cf2.metric("Net Cash Movement", f"Rs {net_cash_movement:,.2f}")
cf3.metric("Ending Balance", f"Rs {cash_end:,.2f}")

cf_df = pd.DataFrame({
    "Label": ["Beginning Balance", "Net Cash Movement", "Ending Balance"],
    "Amount": [cash_start, net_cash_movement, cash_end]
})

fig_cf = px.bar(cf_df, x="Label", y="Amount", text="Amount",
                title="Cash Flow Overview", color="Label")
fig_cf.update_traces(texttemplate='Rs %{text:,.0f}', textposition='outside')
fig_cf.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_cf, use_container_width=True)

# -------------------------------
# Receivables Aging Donut Chart
# -------------------------------
st.markdown("---")
st.subheader("📊 Receivables Aging Breakdown")

aging_data = {
    "Aging Bucket": ["1–30 Days", "31–60 Days", "61–90 Days", "91–120 Days", "Over 120 Days"],
    "Amount": [950_000, 600_000, 400_000, 150_000, 105_573.10]
}
df_aging = pd.DataFrame(aging_data)

fig_pie = px.pie(
    df_aging,
    names="Aging Bucket",
    values="Amount",
    title="Overdue Balance by Aging",
    hole=0.5
)
fig_pie.update_traces(textinfo='percent+label')
fig_pie.update_layout(height=400, showlegend=True)

st.plotly_chart(fig_pie, use_container_width=True)



# -------------------------------
# 🎯 Customer Overdue Filter
# -------------------------------
st.markdown("---")
st.subheader("🎯 Overdue Balance by Customer")

# Sample customer data (same as earlier)
customer_data = {
    "Customer": [
        "Coral Garden Ltd", "Eric'Seduction", "Lynn and Sea Co Ltd",
        "Mr. Genaro Bhuttoo", "Mr. Jean Eric"
    ],
    "Amount Due": [
        2_205_573.10, 1_200_197.50, 1_526_108.65, 83_100.00, 81_803.45
    ]
}
df_customers = pd.DataFrame(customer_data)

# Dropdown selection
selected_customer = st.selectbox("Select a customer", df_customers["Customer"])

# Show selected customer's data
selected_row = df_customers[df_customers["Customer"] == selected_customer].iloc[0]
st.success(f"💰 {selected_customer} has Rs {selected_row['Amount Due']:,.2f} overdue.")

# Optional: single bar chart for this customer
fig_single = px.bar(
    pd.DataFrame([selected_row]),
    x="Customer",
    y="Amount Due",
    text="Amount Due",
    title="Overdue Amount for Selected Customer"
)

fig_single.update_traces(texttemplate='Rs %{text:,.0f}', textposition='outside')
fig_single.update_layout(showlegend=False, height=300)
st.plotly_chart(fig_single, use_container_width=True)

# -------------------------------
# 📈 Revenue & Net Profit Trend
# -------------------------------
st.markdown("---")
st.subheader("📈 Monthly Revenue & Profit Trend")

# Sample monthly data (manually added — later export from P&L monthly)
monthly_data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Revenue": [800_000, 1_200_000, 1_500_000, 1_100_000, 1_486_420],
    "Net Profit": [400_000, 600_000, 750_000, 550_000, 1_039_726]
}
df_trend = pd.DataFrame(monthly_data)

# Line chart
fig_trend = px.line(
    df_trend,
    x="Month",
    y=["Revenue", "Net Profit"],
    markers=True,
    title="Monthly Revenue vs Net Profit",
    labels={"value": "Amount", "variable": "Metric"}
)

fig_trend.update_layout(height=400)
st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------
# 🎯 Customer Risk Gauge
# -------------------------------
st.markdown("---")
st.subheader("🚦 Customer Risk Gauge")

# Sample mock data (sorted by risk)
risk_data = {
    "Customer": [
        "Coral Garden Ltd", "Eric'Seduction", "Lynn and Sea Co Ltd",
        "Mr. Genaro Bhuttoo", "Mr. Jean Eric"
    ],
    "Overdue Risk Level": [95, 88, 72, 50, 30]  # out of 100
}
df_risk = pd.DataFrame(risk_data)

fig_risk = px.bar(
    df_risk.sort_values(by="Overdue Risk Level"),
    x="Overdue Risk Level",
    y="Customer",
    orientation='h',
    color="Overdue Risk Level",
    color_continuous_scale='RdYlGn_r',
    title="Customer Overdue Risk Level (0 = Safe, 100 = High Risk)"
)

fig_risk.update_layout(height=400)
st.plotly_chart(fig_risk, use_container_width=True)

# -------------------------------
# 🧠 Smart Business Insights
# -------------------------------
st.markdown("---")
st.subheader("🧠 Smart Business Insights")

# Sample logic using mock values
total_receivables = 2_205_573.10
top_3_customers_due = 1_200_197.50 + 1_526_108.65 + 83100.00
cash_end = 7_954_839.88
net_cash_movement = 4_954_839.88
revenue_may = 1_486_420
revenue_apr = 1_100_000

# Generate insights
insights = []

# Top customers hold too much receivables
if top_3_customers_due / total_receivables > 0.75:
    insights.append("⚠️ 3 customers represent more than 75% of all receivables. Consider diversifying.")

# Cash flow
if net_cash_movement > 0:
    insights.append(f"✅ Cash flow is positive this period. Net increase: Rs {net_cash_movement:,.0f}.")
else:
    insights.append("🔴 Cash flow is negative this month. Monitor expenses.")

# Revenue trend
if revenue_may > revenue_apr:
    growth = revenue_may - revenue_apr
    insights.append(f"📈 Revenue increased by Rs {growth:,.0f} compared to last month.")
else:
    insights.append("📉 Revenue has decreased compared to last month.")

# Display insights
for line in insights:
    st.info(line)

# -------------------------------
# 📅 Monthly Filtered KPI View
# -------------------------------
st.markdown("---")
st.subheader("📅 Monthly KPI Filter")

# Mock monthly dataset
monthly_finance = pd.DataFrame({
    "Month": ["January", "February", "March", "April", "May"],
    "Revenue": [800_000, 1_200_000, 1_500_000, 1_100_000, 1_486_420],
    "Net Profit": [400_000, 600_000, 750_000, 550_000, 1_039_726],
    "Cash End": [2_000_000, 3_500_000, 4_100_000, 5_800_000, 7_954_839]
})

# Month selector
selected_month = st.selectbox("Select a month", monthly_finance["Month"])

# Filter row
row = monthly_finance[monthly_finance["Month"] == selected_month].iloc[0]

# Display selected month's KPIs
mk1, mk2, mk3 = st.columns(3)
mk1.metric("Revenue", f"Rs {row['Revenue']:,.0f}")
mk2.metric("Net Profit", f"Rs {row['Net Profit']:,.0f}")
mk3.metric("Cash End", f"Rs {row['Cash End']:,.0f}")

# Show trend again
fig_trend = px.line(
    monthly_finance,
    x="Month",
    y=["Revenue", "Net Profit"],
    markers=True,
    title="Full Trend View",
    labels={"value": "Rs", "variable": "Metric"}
)
fig_trend.update_layout(height=400)
st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------
# 🎯 Business Health Score
# -------------------------------
st.markdown("---")
st.subheader("🧮 Business Health Score")

# Mock scoring inputs (you can later tie to dynamic values)
cash_score = 7_954_839.88
receivables_score = 2_205_573.10
profit_score = 1_039_726

# Score logic
score = 0

if cash_score >= 5_000_000:
    score += 40
elif cash_score >= 2_500_000:
    score += 25
else:
    score += 10

if receivables_score <= 1_000_000:
    score += 30
elif receivables_score <= 2_500_000:
    score += 20
else:
    score += 10

if profit_score >= 800_000:
    score += 30
elif profit_score >= 400_000:
    score += 20
else:
    score += 10

# Status & badge
if score >= 80:
    status = "🟢 Excellent – Business is financially healthy"
elif score >= 60:
    status = "🟡 Moderate – Watch cash and collections"
else:
    status = "🔴 High Risk – Review urgently"

# Display score
st.metric("Business Health Score", f"{score}/100")
st.success(status if "🟢" in status else status)  # shows green if excellent


