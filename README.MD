# Equity Analysis

Equity Analysis is a Python-based project for fetching, analyzing, and visualizing financial market data. It leverages Yahoo Finance for data retrieval, applies statistical and technical indicators for analysis, runs Monte Carlo simulations for forecasting, and generates charts for better insight into market trends.

## Features

- **Data Retrieval:** Uses `yfinance` to fetch historical stock market data.
- **Technical Analysis:** Implements indicators like Moving Averages, RSI, ATR, MACD, Bollinger Bands, and Sharpe Ratio.
- **Fundamental Analysis:** Retrieves key financial metrics, including income statements, balance sheets, and analyst targets.
- **Monte Carlo Simulations:** Performs Monte Carlo-based stock price forecasting and risk analysis.
- **Risk/Reward Analysis:** Evaluates probability distributions for different price targets and computes risk/reward ratios.
- **Visualization:** Generates candlestick and line charts using `mplfinance` and `matplotlib`.
- **Index Correlation Analysis:** Computes and visualizes correlation between stock prices and global indices.
- **Data Normalization:** Supports Min-Max Scaling, Z-score normalization, and percentage change transformations.

## Installation

### Prerequisites
Make sure you have Python installed. You can install required dependencies using:

```sh
pip install -r requirements.txt
```

### Required Libraries
The project uses the following Python libraries:
- `yfinance`
- `numpy`
- `pandas`
- `matplotlib`
- `mplfinance`
- `scipy`
- `seaborn`
- `sklearn`

## Usage

The entire analysis workflow can be executed using `main.py`. This script fetches stock and index data, applies technical and fundamental analysis, runs Monte Carlo simulations, generates charts, and performs risk/reward assessments.

### Running the Main Script
```sh
python main.py
```

### Functionality in `main.py`
```python
import data_request, charts, vis_analytics, analytics, MCS, indices

# Define stock ticker
ticker = 'MS'

# Fetch fundamental data
basic_info = data_request.basic_analysis(ticker)
print(basic_info)

# Retrieve historical stock data
data_15m, data_1h, data_1d, data_1w, data_1m = data_request.request_all_data(ticker)

# Perform technical analysis
vis_analytics.add_to_csv()
charts.generate_charts(data_15m, data_1h, data_1d, data_1w, data_1m, ticker)

# Monte Carlo Simulation
forecast = MCS.prediction_mcs(data_1d)
median_price, lower_bound, upper_bound = MCS.conf_intervals(forecast)
prob = MCS.probability_of_target(forecast, 150)
print(f'Probability of target = {prob} %')

# Risk and Probability Analysis
last_price = data_1h["Close"].dropna().iloc[-1]
probability_df = MCS.probability_distribution(forecast, last_price)

take_profit = last_price * 1.2
stop_loss = last_price * 0.8
risk_reward_result = MCS.risk_reward_analysis(forecast, last_price, take_profit, stop_loss)
print(risk_reward_result)

# Volatility Analysis
historical_volatility = analytics.calculate_historical_volatility(data_1d)
stress_factor = 1.5  # Increase volatility by 50%
max_price_multiplier = 3  # Limit price growth to 3x the initial price

stressed_forecast_log = MCS.stress_test_mcs(forecast, historical_volatility, stress_factor, max_price_multiplier, use_log_normal=True)
stressed_forecast_norm = MCS.stress_test_mcs(forecast, historical_volatility, stress_factor, max_price_multiplier, use_log_normal=False)

# Index Correlation Analysis
data_request.request_indices()
indices_df = indices.prepare_indices(ticker)
indices.indices_corr(indices_df, "pearson", ticker)
indices.indices_corr(indices_df, "spearman", ticker)
indices.indices_corr(indices_df, "kendall", ticker)
```

## Project Structure

```
📦 equity_analysis
├── data/             # Directory for storing CSV files
├── financial_data/   # Directory for storing fundamental financial data
├── plots/            # Directory for saving generated charts
├── data_request.py   # Fetches stock data and fundamental analysis
├── indices.py        # Index correlation analysis and normalization
├── vis_analytics.py  # Implements technical analysis indicators
├── charts.py         # Generates candlestick and line charts
├── analytics.py      # Computes historical volatility and risk analysis
├── MCS.py            # Monte Carlo simulation for stock price prediction
├── utils.py          # Handles data, charts, and report cleanup
├── main.py           # Main script executing the entire analysis pipeline
├── requirements.txt  # Dependencies list
└── LICENSE.MD        # License documentation
```

## License
This project is open-source and available under the GNU General Public License (GPL-3.0).

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Author
**Nikita Manaenkov**

