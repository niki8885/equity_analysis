import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, pacf, acf
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

save_dir = "../data/plots"


def find_q(series, max_lags=5):
    """Find optimal q (MA order) based on ACF values."""
    acf_values = acf(series.dropna().values, nlags=min(max_lags, len(series) - 1))
    for i in range(1, len(acf_values)):
        if abs(acf_values[i]) < (2 / (len(series) ** 0.5)):
            return i - 1
    return min(max_lags, len(series) - 1)


def find_p(series, max_lags=5):
    """Find optimal p (AR order) based on PACF values."""
    pacf_values = pacf(series.dropna().values, nlags=min(max_lags, len(series) - 1))
    for i in range(1, len(pacf_values)):
        if abs(pacf_values[i]) < (2 / (len(series) ** 0.5)):
            return i - 1
    return min(max_lags, len(series) - 1)


def adf_test(series, d=0, column="Close"):
    """Check for stationarity using the ADF test and apply differencing if needed."""
    result = adfuller(series[column].dropna())

    if result[1] <= 0.05:
        return series, d
    else:
        series[f"{column}_diff"] = series[column].diff().dropna()
        return adf_test(series.dropna(), d + 1, column=f"{column}_diff")


def arima_model(ticker):
    """Load data, convert it to daily frequency, and check for stationarity."""
    data = pd.read_csv("../data/raw_data/data_1d.csv", parse_dates=["Date"], index_col="Date")
    data = data[["Close"]].dropna()

    # Explicitly set frequency
    data = data.asfreq('D')

    # ADF Test for differencing order (d)
    data, d = adf_test(data, d=0, column="Close")

    # Extract Close column as a Series
    close_series = data["Close"]

    # Find p and q
    q, p = find_q(close_series, max_lags=5), find_p(close_series, max_lags=5)

    # Reset index to avoid datetime issues
    data_reset = data.reset_index()

    # Fit ARIMA Model
    model = ARIMA(data_reset["Close"], order=(p, d, q), enforce_stationarity=False, enforce_invertibility=False)

    try:
        model_fit = model.fit()
        if not model_fit.mle_retvals['converged']:
            print("⚠️ Warning: ARIMA model did NOT converge properly.")
    except Exception as e:
        print(f"ARIMA model failed to converge: {e}")
        return

    # Forecasting
    forecast_steps = 10  # Predict next 10 days
    forecast_values = model_fit.forecast(steps=forecast_steps)

    forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

    forecast_df = pd.DataFrame(forecast_values.values, index=forecast_index, columns=["Forecast"])
    forecast_df["Close"] = forecast_df["Forecast"]
    forecast_df["Close_diff"] = forecast_df["Close"].diff()

    # Save forecast results to CSV
    filename = f"forecast_results_arima_{ticker}.csv"
    raw_data_dir = "../data/raw_data"
    file_path = os.path.join(raw_data_dir, filename)
    forecast_df.to_csv(file_path, index=True)

    plt.figure(figsize=(12, 6))
    plt.plot(forecast_df["Forecast"], label="Predicted Close", linestyle="dashed", color="red")

    plt.title(f"ARIMA Forecast for {ticker}")

    plt.xlabel("Date")
    plt.ylabel("Predicted Close Price")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(save_dir, f"ARIMA Forecast for {ticker}")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')

    return forecast_df


def find_garch_q(series, max_lags=5):
    """Find optimal q (ARCH order) based on ACF of squared returns."""
    squared_series = series.dropna() ** 2  # GARCH models use squared returns
    acf_values = acf(squared_series.values, nlags=min(max_lags, len(series) - 1))

    for i in range(1, len(acf_values)):
        if abs(acf_values[i]) < (2 / (len(series) ** 0.5)):  # Significance threshold
            return i - 1

    return min(max_lags, len(series) - 1)


def find_garch_p(series, max_lags=5):
    """Find optimal p (GARCH order) based on PACF of squared returns."""
    squared_series = series.dropna() ** 2  # Use squared log returns
    pacf_values = pacf(squared_series.values, nlags=min(max_lags, len(series) - 1))

    for i in range(1, len(pacf_values)):
        if abs(pacf_values[i]) < (2 / (len(series) ** 0.5)):  # Significance threshold
            return i - 1

    return min(max_lags, len(series) - 1)


def garch_model(ticker):
    # Load data
    data = pd.read_csv("../data/raw_data/data_1d.csv")

    # Adjust close prices
    data["Adj Close"] = data["Close"] * (data["Close"] / data["Close"].shift(1))

    # Compute log returns
    data["Log return"] = np.log(data["Adj Close"] / data["Adj Close"].shift(1))

    # Handle NaN and Inf values
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # Ensure index is datetime for better visualization
    data.index = pd.to_datetime(data.index)

    # Find optimal p and q
    best_p = find_garch_p(data["Log return"])
    best_q = find_garch_q(data["Log return"])

    print(f"Optimal GARCH(p,q): ({best_p}, {best_q})")

    # Fit the GARCH model
    garch_model = arch_model(data["Log return"] * 100, vol="Garch", p=best_p, q=best_q, mean="Zero", dist="normal")
    garch_result = garch_model.fit(disp="off")

    print(garch_result.summary())

    # Extract volatility
    data["Volatility"] = np.sqrt(garch_result.conditional_volatility)

    # Plot estimated volatility
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data["Volatility"], color="red", label="GARCH Estimated Volatility")
    plt.xlabel("Date")
    plt.title(f"{ticker} Estimated Volatility from GARCH Model")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(save_dir, f"{ticker} Estimated Volatility from GARCH Model")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')

    # Forecast future volatility
    forecast_horizon = 30
    forecast = garch_result.forecast(horizon=forecast_horizon)

    # Extract variance forecast
    predicted_vol = np.sqrt(forecast.variance.values[-1, :])

    # Plot predicted volatility
    plt.figure(figsize=(10, 4))
    plt.plot(predicted_vol, marker="o", label="Predicted Volatility")
    plt.title(f"{ticker} GARCH 30-Day Volatility Forecast")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(save_dir, f"{ticker} GARCH 30-Day Volatility Forecast")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')

    # Rolling volatility for comparison
    data["Rolling Volatility"] = data["Log return"].rolling(window=30).std() * 100

    # 🚨 Identify the index with the highest rolling volatility
    spike_index = data["Rolling Volatility"].idxmax()

    # Plot volatility comparison
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data["Volatility"], color="red", label="GARCH Volatility")
    plt.plot(data.index, data["Rolling Volatility"], linestyle="dashed", color="blue", label="Rolling Volatility (30-day)")

    # Add a vertical line at the spike in volatility
    if not pd.isna(spike_index):  # Ensure it's a valid index
        plt.axvline(x=spike_index, color="gray", linestyle="dotted", label="Volatility Spike")

    plt.title(f"{ticker} Volatility Comparison")
    plt.xlabel("Date")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(save_dir, f"{ticker} Volatility Comparison")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')

    # ✅ Value at Risk (VaR) Calculation
    confidence_level = 0.95  # 95% Confidence
    z_score = 1.645  # Z-score for 95% confidence

    VaR = predicted_vol[-1] * z_score  # Estimate worst-case loss

    print(f"1-Day 95% VaR Estimate: {VaR:.2f}%")


# TODO: Arima testing
