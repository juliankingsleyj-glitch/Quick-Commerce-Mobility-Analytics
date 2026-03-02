# Micro-Mobility Fleet Dispatch & Quick-Commerce Analytics

This repository contains in-depth Python scripts demonstrating advanced data analytics, hypothesis testing, and inventory optimization tailored to Micro-Mobility (e.g., Yulu) and Quick-Commerce (e.g., Blinkit, Ola) industries.

## 1. Micro-Mobility Fleet Dispatch Analytics (`mobility_analytics.py`)

**Objective:**
Optimize algorithmic fleet dispatch logic by deploying rigorous SciPy hypothesis testing (ANOVA, Chi-Square) on extensive mobility datasets to mathematically prove the impact of weather variables on supply-side drop-offs.

**Methodology:**
- **Synthetic Data Generation:** Simulates a realistic micro-mobility dataset with 10,000 hourly records including weather conditions (Clear, Cloudy, Light Rain, Heavy Rain, Thunderstorm), total fleet, and supply-side drop-offs.
- **SQL Aggregation:** Uses SQLite to simulate data warehousing queries, summarizing average fleet availability and drop-off ratios per weather condition.
- **SciPy Hypothesis Testing:**
  - **ANOVA:** Tests the null hypothesis that the mean supply drop-off ratio is equal across all weather conditions.
  - **Chi-Square Test:** Tests the association between extreme weather events and high supply drop-off occurrences (>20% drop-off).
- **Outcome:** Provides mathematical proof to adjust dynamic fleet re-allocation strategies based on forecasted adverse weather.

## 2. Quick-Commerce Inventory Analytics (`qcomm_analytics.py`)

**Objective:**
Maximize revenue yield per square foot by analyzing large-scale FMCG retail datasets using Python (Pandas) to formulate hyper-local inventory distribution strategies based on demand velocity.

**Methodology:**
- **Synthetic Data Generation:** Simulates a hyper-local network of "dark stores" (Blinkit/Ola model) recording daily sales volume and revenue across various FMCG categories (Fresh Produce, Dairy, Snacks, etc.) over 30 days.
- **SQL Data Pipeline:** Aggregates store-level data to calculate total sales and revenue per category.
- **Pandas Data Processing:**
  - Calculates **Demand Velocity** (sales volume per day).
  - Calculates **Revenue Yield per Square Foot**.
- **Hyper-Local Distribution Strategy:** Categorizes products dynamically into 4 quadrants based on median velocity and yield thresholds:
  - *High Priority:* Maximize Shelf Space & Reorder Frequency.
  - *Volume Driver:* Optimize for Bulk Storage (Back-room).
  - *Margin Driver:* Premium Shelf Placement (Eye-level).
  - *Low Priority:* Minimum Inventory / On-Demand Sourcing.
- **Outcome:** Recommends optimized shelf-space allocation and dark store layout to maximize total revenue yield.

## Running the Scripts

Ensure you have the required libraries installed:
```bash
pip install pandas numpy scipy
```

**Run Mobility Analytics:**
```bash
python mobility_analytics.py
```

**Run Quick-Commerce Analytics:**
```bash
python qcomm_analytics.py
```