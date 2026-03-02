Enterprise Fleet Dispatch & Hyper-Local Quick Commerce Analytics

# Executive Summary

This repository contains advanced Python and SQL analytics pipelines designed to solve two major operational bottlenecks in the micro-mobility (e.g., Yulu, Ola) and quick-commerce (e.g., Blinkit, Zepto) sectors: weather-induced fleet supply drop-offs and dark store inventory optimization.

By applying rigorous inferential statistics (ANOVA, Chi-Square) and dynamic demand velocity tracking, this project transitions operations from "gut-feeling" heuristics to mathematically proven, data-driven supply chain strategies.

# Part 1: Micro-Mobility Fleet Dispatch Analytics

File: mobility_analytics.py

The Business Challenge

Operations managers frequently rely on intuition to anticipate how adverse weather impacts supply-side rider availability. This results in either over-subsidizing idle riders or facing severe demand unfulfillment during sudden weather shifts.

Analytical Architecture

Data Pipeline: Ingests an anonymized, large-scale mobility dataset (10,000+ hourly records) mapping localized weather patterns (Clear, Light Rain, Heavy Rain, Thunderstorm) against total fleet availability.

SQL Aggregation: Utilizes a localized SQLite environment to execute data warehousing queries, summarizing average fleet availability and isolating supply-side drop-off ratios.

Hypothesis Testing (SciPy):

ANOVA: Deployed to test the null hypothesis across 4+ weather categories, mathematically proving the variance in supply drop-offs is statistically significant and not random noise.

Chi-Square Test: Validates the association between extreme weather events and critical supply failures (>20% drop-off).

Strategic ROI

Provides the statistical proof required for dynamic fleet re-allocation. Operations teams can now integrate this logic into their dispatch algorithms to proactively surge pricing or incentivize riders before the weather impacts fulfillment.

# Part 2: Quick-Commerce Hyper-Local Inventory Analytics

File: qcomm_analytics.py

The Business Challenge

In the quick-commerce "dark store" model, shelf space is highly constrained and extremely expensive. Storing low-velocity items in premium eye-level shelving drastically reduces overall profitability.

Analytical Architecture

Data Pipeline: Ingests a 30-day FMCG retail dataset mapping daily sales volume, revenue yield, and category classifications across a hyper-local dark store network.

Pandas Processing: - Computes the Demand Velocity (unit sales per day) for hundreds of SKUs.

Computes the Revenue Yield per Square Foot to determine spatial efficiency.

Dynamic Quadrant Mapping: Algorithmically categorizes FMCG products into four distinct actionable quadrants based on median velocity and yield thresholds.

Strategic ROI

Generates a mathematically backed floor-plan optimization strategy:

High Priority (High Yield / High Velocity): Maximize premium shelf space & reorder frequency.

Volume Driver (Low Yield / High Velocity): Optimize for bulk, back-room storage.

Margin Driver (High Yield / Low Velocity): Premium front-store placement; maintain lower inventory depth.

Low Priority (Low Yield / Low Velocity): Minimum inventory / transition to on-demand sourcing.

# Technical Execution

Prerequisites

Ensure your local environment has the required scientific computing libraries installed:

pip install pandas numpy scipy sqlite3


# Running the Pipelines

Execute the analytical scripts via the command line. The scripts will output the statistical p-values, demand velocity matrices, and strategic recommendations directly to the console.

1. Run Fleet Dispatch Analytics:

python mobility_analytics.py


2. Run Dark Store Inventory Analytics:

python qcomm_analytics.py
