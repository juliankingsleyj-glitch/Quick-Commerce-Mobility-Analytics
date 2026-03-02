import pandas as pd
import numpy as np
import sqlite3
import scipy.stats as stats
import warnings
warnings.filterwarnings('ignore')

def generate_yulu_dataset(num_records=10000):
    """
    Generates a synthetic dataset mimicking Yulu's micro-mobility operations.
    """
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', periods=num_records, freq='h')
    
    weather_conditions = ['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Thunderstorm']
    # Probabilities for weather
    weather_probs = [0.5, 0.3, 0.1, 0.08, 0.02]
    
    weather = np.random.choice(weather_conditions, size=num_records, p=weather_probs)
    
    # Base fleet available
    total_fleet = np.random.randint(500, 1000, size=num_records)
    
    # Drop-off logic based on weather (worse weather = more drop-offs/less supply available)
    drop_off_rates = {
        'Clear': 0.05,
        'Cloudy': 0.10,
        'Light Rain': 0.25,
        'Heavy Rain': 0.50,
        'Thunderstorm': 0.75
    }
    
    # Add some noise to the drop-off rates
    drop_offs = []
    for w, tf in zip(weather, total_fleet):
        base_rate = drop_off_rates[w]
        actual_rate = max(0, min(1, np.random.normal(base_rate, 0.05)))
        drop_offs.append(int(tf * actual_rate))
        
    df = pd.DataFrame({
        'timestamp': dates,
        'weather_condition': weather,
        'total_fleet': total_fleet,
        'supply_drop_offs': drop_offs
    })
    
    df['available_fleet'] = df['total_fleet'] - df['supply_drop_offs']
    df['drop_off_ratio'] = df['supply_drop_offs'] / df['total_fleet']
    
    return df

def run_mobility_analytics():
    print("=== Micro-Mobility Fleet Dispatch Analytics (Yulu) ===")
    
    # 1. Generate Dataset
    df = generate_yulu_dataset()
    print(f"Generated {len(df)} records of mobility data.")
    
    # 2. SQL Context - Load into SQLite to simulate data warehousing
    conn = sqlite3.connect(':memory:')
    df.to_sql('mobility_data', conn, index=False)
    
    query = """
        SELECT 
            weather_condition,
            COUNT(*) as record_count,
            AVG(total_fleet) as avg_total_fleet,
            AVG(supply_drop_offs) as avg_drop_offs,
            AVG(drop_off_ratio) as avg_drop_off_ratio
        FROM mobility_data
        GROUP BY weather_condition
        ORDER BY avg_drop_off_ratio ASC
    """
    
    summary_df = pd.read_sql(query, conn)
    print("\n--- SQL Aggregation: Average Drop-offs by Weather ---")
    print(summary_df.to_string(index=False))
    
    # 3. Hypothesis Testing using SciPy
    print("\n--- Statistical Analysis (SciPy) ---")
    
    # A. ANOVA Test
    # Null Hypothesis: The mean supply drop-off ratio is the same across all weather conditions.
    # Alternative Hypothesis: At least one weather condition has a different mean drop-off ratio.
    
    weather_groups = [group['drop_off_ratio'].values for name, group in df.groupby('weather_condition')]
    f_stat, p_val = stats.f_oneway(*weather_groups)
    
    print("\n1. ANOVA Test on Supply Drop-off Ratio across Weather Conditions")
    print(f"F-Statistic: {f_stat:.4f}")
    print(f"P-Value: {p_val:.4e}")
    if p_val < 0.05:
        print("Conclusion: Reject Null Hypothesis. Weather conditions significantly impact supply-side drop-offs.")
    else:
        print("Conclusion: Fail to Reject Null Hypothesis. Weather conditions do not significantly impact supply-side drop-offs.")
        
    # B. Chi-Square Test for Independence
    # Categorize drop-off ratio into High (>20%) and Low (<=20%)
    df['high_drop_off'] = np.where(df['drop_off_ratio'] > 0.20, 'Yes', 'No')
    
    # Create contingency table
    contingency_table = pd.crosstab(df['weather_condition'], df['high_drop_off'])
    print("\n2. Contingency Table for Chi-Square Test (Weather vs High Drop-off Rate):")
    print(contingency_table)
    
    chi2_stat, p_val_chi2, dof, expected = stats.chi2_contingency(contingency_table)
    
    print(f"\nChi-Square Statistic: {chi2_stat:.4f}")
    print(f"P-Value: {p_val_chi2:.4e}")
    print(f"Degrees of Freedom: {dof}")
    
    if p_val_chi2 < 0.05:
        print("Conclusion: Reject Null Hypothesis. There is a significant association between weather conditions and experiencing high supply drop-offs.")
    else:
        print("Conclusion: Fail to Reject Null Hypothesis. No significant association found.")
        
    print("\n--- Optimization Strategy ---")
    print("Based on these findings, algorithmic fleet dispatch logic must dynamically re-allocate buffer supply")
    print("to high-demand zones pre-emptively when adverse weather (e.g., Heavy Rain, Thunderstorm) is forecasted,")
    print("as these conditions mathematically prove to cause statistically significant supply-side drop-offs.")

if __name__ == "__main__":
    run_mobility_analytics()
