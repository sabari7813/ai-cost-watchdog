import pandas as pd

df = pd.read_csv('ai_usage_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date

DAILY_COST_LIMIT = 0.70

today_cost = df.groupby('date')['cost_usd'].sum()
max_day_cost = today_cost.max()

print("===== 🔔 ALERT SYSTEM =====")

if max_day_cost > DAILY_COST_LIMIT:
    print(f"🚨 ALERT! Peak day cost ${max_day_cost:.3f} exceeded limit ${DAILY_COST_LIMIT}!")
else:
    print(f"✅ Cost Normal: ${max_day_cost:.3f}")

# Session timeout alert
long_sessions = df[df['session_duration_min'] > 45]
if not long_sessions.empty:
    print(f"⏰ WARNING: {len(long_sessions)} sessions ran >45 mins!")

# Error rate alert
error_pct = (df['status'] != 'success').mean() * 100
if error_pct > 15:
    print(f"❌ High Error Rate: {error_pct:.1f}% - Investigate!")
else:
    print(f"✅ Error Rate OK: {error_pct:.1f}%")

# Most expensive model
model_cost = df.groupby('model')['cost_usd'].sum()
expensive_model = model_cost.idxmax()
print(f"💸 Most Expensive Model: {expensive_model} (${model_cost.max():.2f})")

print("\n===== ✅ MONITORING COMPLETE =====")