# Equity Analysis

Equity Analysis is a Python-based project for fetching, analyzing, and visualizing financial market data. It leverages Yahoo Finance for data retrieval, applies statistical and technical indicators for analysis, runs Monte Carlo simulations for forecasting, and generates charts for better insight into market trends.

## Features

- **Data Retrieval:** Uses `yfinance` to fetch historical stock market data.
- **Technical Analysis:** Implements indicators like Moving Averages, RSI, ATR, MACD, Bollinger Bands, and Sharpe Ratio.
- **Fundamental Analysis:** Retrieves key financial metrics, including income statements, balance sheets, and analyst targets.
- **Monte Carlo Simulations:** Performs Monte Carlo-based stock price forecasting and risk analysis.
- **Risk/Reward Analysis:** Evaluates probability distributions for different price targets and computes risk/reward ratios.
- **Visualization:** Generates candlestick and line charts using `mplfinance` and `matplotlib`.

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

## Usage

### Fetching Data
```python
import data_request

ticker = 'MS'
data = data_request.request_data(ticker, "1d", start_days=30, save=True, filename="data_1d.csv")
```

### Performing Basic Analysis
```python
basic_info = data_request.basic_analysis(ticker)
print(basic_info["info"])  # Prints fundamental information about the stock
```

### Applying Technical Indicators
```python
import vis_analytics

rsi = vis_analytics.relative_strength_index(data)
macd_line, signal_line = vis_analytics.macd(data)
```

### Generating Charts
```python
import charts

charts.candlestick_chart(data, "Daily Candlestick Chart")
charts.lineplot_chart(data, "Daily Line Chart")
```

### Running Monte Carlo Simulations
```python
import MCS

forecast = MCS.prediction_mcs(data, days=30, simulations=1000)
MCS.conf_intervals(forecast)
```

### Risk and Probability Analysis
```python
current_price = data['Close'].iloc[-1]
probability_distribution = MCS.probability_distribution(forecast, current_price)
```

### Volatility Analysis
```python
import analytics

historical_volatility = analytics.calculate_historical_volatility(data)
```

## Project Structure

```
📦 equity_analysis
├── data/             # Directory for storing CSV files
├── data_request.py   # Fetches stock data and fundamental analysis
├── vis_analytics.py  # Implements technical analysis indicators
├── charts.py         # Generates candlestick and line charts
├── MCS.py            # Monte Carlo simulation for stock price prediction
├── analytics.py      # Computes historical volatility and risk analysis
├── main.py           # Example script for running the analysis
├── requirements.txt  # Dependencies list
└── README.md         # Documentation
```

## License
This project is open-source and available under the MIT License.

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Author
**Nikita Manaenkov**



