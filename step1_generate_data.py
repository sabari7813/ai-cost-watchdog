import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)

models = ['gpt-4', 'claude-sonnet', 'gemini-pro']
users = ['user_A', 'user_B', 'user_C', 'user_D']

data = []
for _ in range(500):
    model = random.choice(models)
    tokens = random.randint(100, 4000)
    cost_per_token = {'gpt-4': 0.00003, 'claude-sonnet': 0.000015, 'gemini-pro': 0.000010}
    data.append({
        'timestamp': fake.date_time_between('-30d', 'now'),
        'user': random.choice(users),
        'model': model,
        'tokens_used': tokens,
        'cost_usd': round(tokens * cost_per_token[model], 4),
        'session_duration_min': random.randint(1, 60),
        'status': random.choice(['success', 'success', 'success', 'timeout', 'error'])
    })

df = pd.DataFrame(data)
df.sort_values('timestamp', inplace=True)
df.to_csv('ai_usage_data.csv', index=False)
print("✅ Data Generated Successfully!")
print(df.head())