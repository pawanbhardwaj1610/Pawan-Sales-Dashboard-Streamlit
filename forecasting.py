import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("dataset/sales_data_project_dataset.csv")

# Fix date column
data['order_date'] = pd.to_datetime(data['order_date'], format='mixed', dayfirst=True)

# Convert sales column to numeric
data['sales'] = data['sales'].astype(str).str.replace(',', '')
data['sales'] = pd.to_numeric(data['sales'], errors='coerce')

# Group sales by date
daily_sales = data.groupby('order_date')['sales'].sum().reset_index()

# Create numeric index
daily_sales['days'] = np.arange(len(daily_sales))

# Training data
X = daily_sales[['days']]
y = daily_sales['sales']

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict next 90 days
future_days = np.arange(len(daily_sales), len(daily_sales) + 90).reshape(-1,1)

predictions = model.predict(future_days)

print("Next 90 Days Sales Forecast:")
print(predictions)

# Plot result
plt.figure(figsize=(10,5))
plt.plot(daily_sales['days'], y, label="Actual Sales")
plt.plot(future_days, predictions, label="Forecasted Sales")

plt.title("Sales Forecast")
plt.xlabel("Days")
plt.ylabel("Sales")
plt.legend()
plt.show()
