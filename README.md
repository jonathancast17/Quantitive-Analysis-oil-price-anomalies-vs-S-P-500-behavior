# Quantitive-Analysis-oil-price-anomalies-vs-S-P-500-behavior
Quantitative analysis: oil price anomalies vs S&amp;P 500 behavior using Z-Score and historical backtesting
WTI Crude Oil vs S&P 500 — Anomaly Detection Analysis

## Quantitative analysis of the correlation between extreme oil price 
movements and S&P 500 behavior in the following 48 hours.

## What it does
- Downloads 10 years of real market data (WTI, S&P 500, US10Y Bonds)
- Identifies Mondays with oil price spikes above 7%
- Calculates Z-Score to detect statistical anomalies
- Computes historical probability of S&P 500 movement after oil spikes
- Visualizes potential Credit Crunch signals (Oil vs Bonds)

## Key Results (March 09, 2026)
- 5 historical events identified since 2015
- Historical probability: S&P 500 drops 60% of the time
  in the 48h following an oil spike Monday
- Current Z-Score: 0.70σ — movement within normal ranges

## Tech Stack
Python · yfinance · matplotlib · numpy · pandas
