import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('ai_usage_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

daily_cost = df.groupby('date')['cost_usd'].sum().reset_index()
model_cost = df.groupby('model')['cost_usd'].sum().reset_index()
user_usage = df.groupby('user')['tokens_used'].sum().reset_index()
hourly = df.groupby('hour')['tokens_used'].sum()
status_counts = df['status'].value_counts()

fig = plt.figure(figsize=(16, 10))
fig.suptitle('AI Usage & Cost Monitor Dashboard', fontsize=18, fontweight='bold')
gs = gridspec.GridSpec(2, 3, figure=fig)

# 1. Daily Cost Trend
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(range(len(daily_cost)), daily_cost['cost_usd'], color='royalblue', marker='o')
ax1.axhline(y=daily_cost['cost_usd'].mean()*1.5, color='red', linestyle='--', label='Alert Threshold')
ax1.set_title('Daily Cost Trend (USD)')
ax1.set_ylabel('Cost (USD)')
ax1.legend()

# 2. Cost by Model
ax2 = fig.add_subplot(gs[0, 2])
ax2.pie(model_cost['cost_usd'], labels=model_cost['model'], autopct='%1.1f%%',
        colors=['#FF6B6B','#4ECDC4','#45B7D1'])
ax2.set_title('Cost by Model')

# 3. Tokens by User
ax3 = fig.add_subplot(gs[1, 0])
ax3.bar(user_usage['user'], user_usage['tokens_used'], color='mediumseagreen')
ax3.set_title('Tokens Used per User')
ax3.set_ylabel('Total Tokens')

# 4. Hourly Usage
ax4 = fig.add_subplot(gs[1, 1])
ax4.bar(hourly.index, hourly.values, color='mediumpurple')
ax4.set_title('Usage by Hour of Day')
ax4.set_xlabel('Hour')

# 5. Status Breakdown
ax5 = fig.add_subplot(gs[1, 2])
ax5.bar(status_counts.index, status_counts.values,
        color=['green','orange','red'])
ax5.set_title('API Call Status')

plt.tight_layout()
plt.savefig('ai_dashboard.png', dpi=150)
print("Dashboard saved as ai_dashboard.png!")
plt.show()