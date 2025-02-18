import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, pacf, acf
from statsmodels.tsa.arima.model import ARIMA

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

# TODO: Arima testing
# TODO: Make Generalized Autoregressive Conditional Heteroskedasticity