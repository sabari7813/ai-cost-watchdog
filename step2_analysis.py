import pandas as pd

df = pd.read_csv('ai_usage_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

# Daily cost
daily_cost = df.groupby('date')['cost_usd'].sum().reset_index()

# Per model cost
model_cost = df.groupby('model')['cost_usd'].sum().reset_index()

# Per user usage
user_usage = df.groupby('user')['tokens_used'].sum().reset_index()

# Error rate
error_rate = df['status'].value_counts(normalize=True) * 100

print("===== 📊 ANALYSIS RESULTS =====")
print(f"\n💰 Total Cost: ${df['cost_usd'].sum():.2f} USD")
print(f"\n📅 Daily Cost:\n{daily_cost}")
print(f"\n🤖 Cost by Model:\n{model_cost}")
print(f"\n👤 Tokens by User:\n{user_usage}")
print(f"\n⚠️ Status Rate:\n{error_rate}")