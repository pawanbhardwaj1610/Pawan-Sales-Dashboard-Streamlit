import pandas as pd

data = pd.read_csv("dataset/sales_data_project_dataset.csv")

# handle mixed date formats
data['order_date'] = pd.to_datetime(data['order_date'], format='mixed', dayfirst=True)

print("Dataset Shape:", data.shape)

print("\nColumns:")
print(data.columns)

# total sales
total_sales = data['sales'].sum()
print("\nTotal Sales:", total_sales)

# total profit
total_profit = data['profit'].sum()
print("Total Profit:", total_profit)

# region analysis
region_sales = data.groupby('region')['sales'].sum()

print("\nSales by Region:")
print(region_sales)
