# HarvestLink

## Project Summary

HarvestLink is a Smart Agriculture Decision Support System designed to assist farmers in making data-driven decisions related to market timing, storage allocation, and transport logistics. The system integrates market intelligence, storage recommendation, and transport optimization to generate explainable, actionable recommendations tailored to farmer needs.

HarvestLink uses offline CSV data sources for flexibility and accessibility in low-connectivity environments.

---

## Features

### Market Intelligence
- Analyzes historical price data for selected crops and mandis.
- Computes trend, volatility, and momentum indicators.
- Provides actionable guidance such as SELL, HOLD, or STORE based on market conditions.

### Storage Recommendation
- Filters storage facilities by crop and available capacity.
- Computes multi-factor scoring including cost, utilization, projected congestion, trust score, and weather risk.
- Outputs ranked storage recommendations with clear reasoning.

### Transport Optimization
- Recommends vehicles based on capacity requirements and optimization priority (cheapest, fastest, eco-friendly).
- Estimates transport cost and CO₂ emissions.
- Facilitates transport booking while managing farmer wallet balance.

### Integrated Decision Engine
- Combines outputs from all modules to deliver a final decision with confidence scoring.
- Provides clear textual explanations supporting decisions.

---

## System Architecture

HarvestLink is composed of the following key modules:

- **Data Ingestion**  
  Loads input data from structured CSV files.

- **Market Module**  
  Performs time series analysis and market trend scoring.

- **Storage Module**  
  Computes multi-objective storage scores.

- **Transport Module**  
  Optimizes vehicle selection based on cost and emissions.

- **Decision Engine**  
  Aggregates scores and generates a final recommendation.

A diagram illustrating the flow between these modules is included in the project documentation.

---

## Data Sources

The project uses structured CSV files as data sources:

- `farmers.csv`: Farmer profiles.
- `crop_profiles.csv`: Crop safe days and ideal storage conditions.
- `market_prices.csv`: Historical pricing data for crops.
- `cold_storage.csv`: Storage facility records.
- `storage_reviews.csv`: Farmer ratings for storage facilities.
- `transport_routes.csv`: Transportation routes with distances.
- `vehicles.csv`: Available vehicle fleet information.
- `farmer_wallets.csv`: Wallet balances for farmers.
- `transport_bookings.csv`: Transport booking records.

The schema for each file is documented in `docs/schema.md`.

---

## Installation and Setup

1. Clone the repository:
