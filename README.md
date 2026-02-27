# Mobility & Quick-Commerce Operational Analytics: Ola & Blinkit

# Summary
This project features a dual-pronged operational analysis of two fast-paced tech sectors: Ride-hailing (Ola) and Hyper-local Quick Commerce (Blinkit). Utilizing SQL for mobility dispatch data and Python (Pandas) for FMCG retail data, the analysis identifies severe operational inefficiencies, isolates supply-side drop-offs (driver cancellations), and formulates hyper-local inventory distribution strategies.

# Business Problem
Hyper-local businesses operate on razor-thin margins and rely heavily on supply-side reliability and optimized physical inventory.
Mobility (Ola): High driver cancellation rates and dispatch delays lead to customer churn and lost Gross Merchandise Value (GMV).
Quick-Commerce (Blinkit): Generic inventory stocking across different city tiers leads to dead stock in some areas and stockouts in others, severely reducing revenue yield per square foot.

# Technical Stack
Database Querying (Mobility): SQL (PostgreSQL, Aggregations, Filtering)
Data Manipulation (Quick-Commerce): Python 3, Pandas, NumPy
Data Visualization: Matplotlib, Seaborn

# Part 1: Mobility Fleet Optimization (SQL - Ola)
To optimize fleet dispatch logic, we need to understand why and where rides are failing. I engineered SQL queries to track driver defection rates and isolate high-value customers for loyalty retention.
1. Isolating Supply-Side Drop-offs (Driver Cancellations)
Understanding why drivers cancel is critical for adjusting algorithmic incentive structures.

-- Calculate total rides cancelled strictly due to supply-side personal/car issues
SELECT 
    Vehicle_Type,
    COUNT(*) AS total_driver_cancellations
FROM ride_data
WHERE Booking_Status = 'Cancelled by Driver' 
  AND Reason_for_cancelling_by_Driver = 'Personal & Car related issues'
GROUP BY Vehicle_Type
ORDER BY total_driver_cancellations DESC;


2. Retaining High-LTV (Lifetime Value) Customers
Identifying the top users allows the business to offer targeted VIP dispatch priority.

-- Isolate the top 5 highest-frequency riders and calculate their total successful GMV
SELECT 
    Customer_ID, 
    COUNT(Booking_ID) AS total_successful_rides,
    ROUND(SUM(Booking_Value)::numeric, 2) As Total_Revenue_Generated
FROM ride_data
WHERE Booking_Status = 'Success'
GROUP BY Customer_ID
ORDER BY total_successful_rides DESC 
LIMIT 5;


# Part 2: Quick-Commerce Inventory Velocity (Python - Blinkit)
For the Blinkit dataset, I used Python's Pandas library to move beyond basic sales totals and calculate hyper-local demand velocity.

1. Analyzing Tier-Specific Demand
Instead of stocking every outlet the same way, we group the data to see exactly how different city tiers behave regarding "Fat Content" and "Item Type."

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset and clean messy data entries
df = pd.read_csv("blinkit_data.csv")
df['Item Fat Content'] = df['Item Fat Content'].replace({'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'})

# Grouping by City Tier and Fat Content to find Hyper-Local Demand Velocity
tier_demand = df.groupby(['Outlet Location Type', 'Item Fat Content']).agg(
    Total_Sales=('Sales', 'sum'),
    Average_Sales=('Sales', 'mean'),
    Volume_Sold=('Item Identifier', 'count')
).reset_index()

print(tier_demand.sort_values(by='Total_Sales', ascending=False))


2. Shelf-Space Allocation by Category Performance
# Identifying the highest-grossing item categories to dictate physical shelf space
item_velocity = df.groupby('Item Type').agg(Total_Sales=('Sales', 'sum')).reset_index()
item_velocity = item_velocity.sort_values(by='Total_Sales', ascending=False)

# Visualizing Top 5 Categories
plt.figure(figsize=(10, 6))
sns.barplot(data=item_velocity.head(5), x='Total_Sales', y='Item Type', palette='Blues_r')
plt.title('Top 5 FMCG Categories by Revenue Velocity')
plt.xlabel('Total Sales ($)')
plt.ylabel('Item Category')
plt.show()


# Strategic Recommendations

Dynamic Driver Incentives (Ola): SQL analysis reveals a high frequency of driver cancellations due to "personal/car issues." Recommend implementing a dynamic micro-bonus for drivers who accept and complete rides in high-cancellation zones to stabilize supply.
Tier 3 Shelf-Space Optimization (Blinkit): Python aggregations show Tier 3 cities process immense volume. Recommend prioritizing shelf space for high-velocity items like "Snack Foods" and "Fruits and Vegetables" over low-performing "Breakfast" items to maximize yield per square foot.
