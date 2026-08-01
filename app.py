import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

st.set_page_config(page_title="AI Usage Dashboard", layout="wide")
st.title("🤖 AI Usage & Cost Monitor Dashboard")

# Load data
df = pd.read_csv('ai_usage_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

# Alert System - Top
st.subheader("🔔 Live Alerts")
DAILY_COST_LIMIT = 0.70
today_cost = df.groupby('date')['cost_usd'].sum()
max_day_cost = today_cost.max()

col1, col2, col3 = st.columns(3)
with col1:
    if max_day_cost > DAILY_COST_LIMIT:
        st.error(f"🚨 Cost Alert! ${max_day_cost:.3f} exceeded ${DAILY_COST_LIMIT}!")
    else:
        st.success(f"✅ Cost Normal: ${max_day_cost:.3f}")

with col2:
    error_pct = (df['status'] != 'success').mean() * 100
    if error_pct > 15:
        st.error(f"❌ High Error Rate: {error_pct:.1f}%")
    else:
        st.success(f"✅ Error Rate OK: {error_pct:.1f}%")

with col3:
    long_sessions = len(df[df['session_duration_min'] > 45])
    if long_sessions > 50:
        st.warning(f"⏰ {long_sessions} Long Sessions!")
    else:
        st.success(f"✅ Sessions Normal")

# Metrics
st.subheader("📊 Key Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Cost", f"${df['cost_usd'].sum():.2f}")
m2.metric("Total Sessions", len(df))
m3.metric("Avg Tokens/Session", f"{df['tokens_used'].mean():.0f}")
m4.metric("Success Rate", f"{(df['status']=='success').mean()*100:.1f}%")

# Charts
st.subheader("📈 Analytics")

col_a, col_b = st.columns(2)

with col_a:
    st.write("**Daily Cost Trend**")
    daily_cost = df.groupby('date')['cost_usd'].sum()
    st.line_chart(daily_cost)

with col_b:
    st.write("**Tokens by User**")
    user_usage = df.groupby('user')['tokens_used'].sum()
    st.bar_chart(user_usage)

col_c, col_d = st.columns(2)

with col_c:
    st.write("**Usage by Hour**")
    hourly = df.groupby('hour')['tokens_used'].sum()
    st.bar_chart(hourly)

with col_d:
    st.write("**Cost by Model**")
    model_cost = df.groupby('model')['cost_usd'].sum()
    st.bar_chart(model_cost)

# Raw Data
st.subheader("📋 Raw Data")
st.dataframe(df.tail(20))