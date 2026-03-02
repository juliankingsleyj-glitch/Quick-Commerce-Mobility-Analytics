import pandas as pd
import numpy as np
import sqlite3
import warnings
warnings.filterwarnings('ignore')

def generate_qcomm_dataset(num_records=5000):
    """
    Generates a synthetic dataset mimicking Blinkit/Ola Quick-Commerce retail operations.
    """
    np.random.seed(123)
    
    # Simulating a hyper-local network of stores
    stores = [f"Store_BLR_{i}" for i in range(1, 11)]
    
    # Store footprint in square feet
    store_sqft = {store: np.random.randint(1500, 3000) for store in stores}
    
    categories = ['Fresh Produce', 'Dairy', 'Snacks', 'Beverages', 'Personal Care', 'Cleaning Supplies']
    
    data = []
    
    # Generate daily sales data for 30 days
    dates = pd.date_range(start='2023-10-01', periods=30, freq='D')
    
    for store in stores:
        sqft = store_sqft[store]
        for date in dates:
            for category in categories:
                # Random base demand per category
                base_demand = np.random.randint(50, 500)
                
                # Assign price per unit based on category
                if category in ['Fresh Produce', 'Dairy']:
                    price = np.random.uniform(20, 100)
                elif category in ['Snacks', 'Beverages']:
                    price = np.random.uniform(10, 50)
                else:
                    price = np.random.uniform(100, 500)
                
                sales_volume = int(max(0, np.random.normal(base_demand, base_demand * 0.2)))
                revenue = sales_volume * price
                
                data.append([date, store, sqft, category, sales_volume, revenue])
                
    df = pd.DataFrame(data, columns=['date', 'store_id', 'sqft', 'category', 'sales_volume', 'revenue'])
    
    return df

def run_qcomm_analytics():
    print("=== Quick-Commerce Inventory Analytics (Blinkit / Ola) ===")
    
    # 1. Generate Dataset
    df = generate_qcomm_dataset()
    print(f"Generated {len(df)} records of FMCG retail data.")
    
    # 2. SQL Context - Load into SQLite to simulate data warehousing
    conn = sqlite3.connect(':memory:')
    df.to_sql('qcomm_data', conn, index=False)
    
    # Calculate Demand Velocity (sales volume per day) and Revenue Yield per Sq Ft
    query = """
        SELECT 
            store_id,
            sqft,
            category,
            SUM(sales_volume) as total_sales_volume,
            SUM(revenue) as total_revenue,
            SUM(sales_volume) / 30.0 as demand_velocity_per_day,
            SUM(revenue) / sqft as revenue_yield_per_sqft
        FROM qcomm_data
        GROUP BY store_id, category, sqft
    """
    
    analytics_df = pd.read_sql(query, conn)
    
    # 3. Pandas Analytics for Hyper-Local Inventory Distribution Strategy
    print("\n--- Hyper-Local Inventory Distribution Strategy ---")
    
    # Categorize products based on demand velocity and revenue yield
    velocity_threshold = analytics_df['demand_velocity_per_day'].median()
    yield_threshold = analytics_df['revenue_yield_per_sqft'].median()
    
    def determine_strategy(row):
        if row['demand_velocity_per_day'] > velocity_threshold and row['revenue_yield_per_sqft'] > yield_threshold:
            return "High Priority: Maximize Shelf Space & Reorder Frequency"
        elif row['demand_velocity_per_day'] > velocity_threshold and row['revenue_yield_per_sqft'] <= yield_threshold:
            return "Volume Driver: Optimize for Bulk Storage (Back-room)"
        elif row['demand_velocity_per_day'] <= velocity_threshold and row['revenue_yield_per_sqft'] > yield_threshold:
            return "Margin Driver: Premium Shelf Placement (Eye-level)"
        else:
            return "Low Priority: Minimum Inventory / On-Demand Sourcing"
            
    analytics_df['strategy'] = analytics_df.apply(determine_strategy, axis=1)
    
    # Summarize strategies across network
    strategy_summary = analytics_df.groupby(['category', 'strategy']).size().reset_index(name='store_count')
    
    print("\nInventory Distribution Strategy by Category (Sample of Network):")
    print(strategy_summary.head(10).to_string(index=False))
    
    print("\n--- Revenue Yield Optimization ---")
    # Identify top performing stores by yield
    store_yield = analytics_df.groupby(['store_id', 'sqft'])['total_revenue'].sum().reset_index()
    store_yield['overall_yield_per_sqft'] = store_yield['total_revenue'] / store_yield['sqft']
    store_yield = store_yield.sort_values(by='overall_yield_per_sqft', ascending=False)
    
    print("\nTop 3 Stores by Revenue Yield per Sq Ft:")
    print(store_yield.head(3).to_string(index=False))
    
    print("\nConclusion:")
    print("By segmenting FMCG retail categories using demand velocity (Pandas) and cross-referencing against footprint (sq ft),")
    print("we formulated a hyper-local strategy that maximizes revenue yield. High-velocity, high-yield items are prioritized")
    print("for premium shelf space, while volume drivers are relegated to bulk storage to optimize the quick-commerce dark store layout.")

if __name__ == "__main__":
    run_qcomm_analytics()
