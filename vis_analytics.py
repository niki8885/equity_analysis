import pandas as pd
import numpy as np
import os

DATA_DIR = "data"

def moving_average(data, period=50):
    """Calculates the moving average (MA) for the given period."""
    return data['Close'].rolling(window=period).mean()

def average_true_range(data, period=14):
    """Calculates the Average True Range (ATR) to measure volatility."""
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    true_range = pd.Series(np.maximum.reduce([high_low, high_close, low_close]), index=data.index)
    return true_range.rolling(window=period).mean()

def relative_strength_index(data, period=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def exponential_moving_average(data, period=12):
    """Calculates the Exponential Moving Average (EMA)."""
    return data['Close'].ewm(span=period, adjust=False).mean()

def macd(data):
    """Calculates the Moving Average Convergence Divergence (MACD)."""
    ema12 = exponential_moving_average(data, 12)
    ema26 = exponential_moving_average(data, 26)
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

def bollinger_bands(data, period=20, k=2):
    """Calculates Bollinger Bands."""
    ma = moving_average(data, period)
    std_dev = data['Close'].rolling(window=period).std()
    upper_band = ma + (k * std_dev)
    lower_band = ma - (k * std_dev)
    return upper_band, lower_band

def sharpe_ratio(data, risk_free_rate=0.01):
    """Calculates the Sharpe Ratio."""
    returns = data['Close'].pct_change()
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / returns.std()

def alpha_beta(asset_returns, market_returns):
    """Calculates Alpha and Beta values."""
    covariance = np.cov(asset_returns, market_returns)[0, 1]
    beta = covariance / np.var(market_returns)
    alpha = np.mean(asset_returns) - beta * np.mean(market_returns)
    return alpha, beta

def pe_ratio(stock_price, earnings_per_share):
    """Calculates the Price-to-Earnings (P/E) ratio."""
    return stock_price / earnings_per_share

def add_to_csv():
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, file)

            df = pd.read_csv(file_path, parse_dates=['Date'])

            df['MA_50'] = moving_average(df, 50)
            df['ATR_14'] = average_true_range(df, 14)
            df['RSI_14'] = relative_strength_index(df, 14)
            df['EMA_12'] = exponential_moving_average(df, 12)
            df['EMA_26'] = exponential_moving_average(df, 26)
            df['MACD'], df['Signal_Line'] = macd(df)
            df['Upper_Band'], df['Lower_Band'] = bollinger_bands(df, 20, 2)
            df['Sharpe_Ratio'] = sharpe_ratio(df)

            df.to_csv(file_path, index=False)
            print(f"Analytics added: {file}")