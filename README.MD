# Equity Analysis

Equity Analysis is a Python-based project for fetching, analyzing, and visualizing financial market data. It retrieves data from Yahoo Finance, applies statistical and technical indicators for analysis, runs Monte Carlo simulations for forecasting, and generates charts for better insight into market trends.

## Features

- **Data Retrieval:** Fetches historical stock market data using yfinance.
- **Technical Analysis:** Implements indicators like Moving Averages, RSI, ATR, MACD, Bollinger Bands, and Sharpe Ratio.
- **Fundamental Analysis:** Retrieves key financial metrics, including income statements, balance sheets, and analyst targets.
- **Monte Carlo Simulations:** Performs Monte Carlo-based stock price forecasting and risk analysis.
- **Risk/Reward Analysis:** Evaluates probability distributions for different price targets and computes risk/reward ratios.
- **Visualization:** Generates candlestick and line charts using mplfinance and matplotlib.
- **Index Correlation Analysis:** Computes and visualizes correlation between stock prices and global indices.
- **Data Normalization:** Supports Min-Max Scaling, Z-score normalization, and percentage change transformations.
- **ARIMA:** Time-series forecasting method that captures trends, seasonality, and noise in stock prices.
- **GARCH (Generalized Autoregressive Conditional Heteroskedasticity):** Models and forecasts financial market volatility.
- **GBM (Geometric Brownian Motion):** Simulates stock price movements using stochastic processes for risk analysis and forecasting.

## Installation

### Prerequisites
Make sure you have Python installed. You can install required dependencies using:

```sh
pip install -r requirements.txt
```

### Required Libraries
The project uses the following Python libraries:
- yfinance
- numpy
- pandas
- matplotlib
- mplfinance
- scipy
- seaborn
- sklearn

## Usage

The entire analysis workflow can be executed using `main.py`. This script fetches stock and index data, applies technical and fundamental analysis, runs Monte Carlo simulations, generates charts, and performs risk/reward assessments.

### Running the Main Script

```sh
python main.py
```

### Functionality in `main.py`

```python
import equity_analysis as ea

ticker = 'MS'
ea.clear_working_folders()
ea.all_data_request(ticker)
ea.request_fin_data(ticker)
ea.get_latest_fundamental(ticker)
ea.get_latest_stock_valuation(ticker)
ea.get_dividend_metrics(ticker)
current_price = ea.price(ticker,"current")
ea.add_analytics_to_df()
ea.generate_charts(ticker)
ea.plot_indicators()
ea.prediction_mcs()
ea.conf_intervals()
ea.probability_of_target (150)
ea.probability_distribution(current_price)
ea.risk_reward_analysis(current_price,150,110)
ea.stress_test_mcs(ticker, stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=True)
ea.stress_test_mcs(ticker, stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=False)
ea.arima_model(ticker)
ea.garch_model(ticker)
ea.gbm_model(ticker)
ea.indices_corr("pearson", ticker)
ea.indices_corr("spearman", ticker)
ea.indices_corr("kendall", ticker)

```

## Project Structure

```
📦 equity_analysis
├── data/                     # Main directory for storing CSV files
│   ├── plots/                # Directory for saving generated charts
│   ├── plots_indicators/     # Directory for saving generated charts with indicators
│   ├── financial_data/       # Directory for storing fundamental financial data
│   ├── raw_data/             # Directory for storing raw stock data
│   ├── reports/              # Directory for saving generated reports
│
├── equity_analysis/          # Python package containing analysis scripts
│   ├── __init__.py           # Marks this directory as a Python package
│   ├── arima_garch.py        # Implements ARIMA and GARCH models
│   ├── GBM.py                # Implements Geometric Brownian Motion for stock simulations
│   ├── data_request.py       # Fetches stock data and fundamental analysis
│   ├── indices.py            # Index correlation analysis and normalization
│   ├── fundamental_analysis.py  # Extracts financial metrics, computes key ratios
│   ├── analytics.py          # Computes historical volatility and risk analysis
│   ├── charts.py             # Generates candlestick and line charts
│   ├── MCS.py                # Monte Carlo simulation for stock price prediction
│   ├── utils.py              # Handles data, charts, and report cleanup
│
├── main.py                   # Main script executing the entire analysis pipeline
├── requirements.txt          # Dependencies list
├── LICENSE.md                # License documentation
├── README.md                 # Project documentation and usage instructions
```

## License
This project is open-source and available under the GNU General Public License (GPL-3.0).

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Author
**Nikita Manaenkov**