import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

save_dir = "../data/plots"


def gbm_model(ticker):
    # Load data
    data = pd.read_csv("../data/raw_data/data_1d.csv")

    # Convert date column to datetime
    data["Date"] = pd.to_datetime(data["Date"])

    # Define simulation period
    first_day = data['Date'].iloc[0]
    last_day = data['Date'].iloc[-1]
    T = (last_day - first_day).days / 365.25  # Convert days to years
    N = len(data)  # Number of time steps (trading days)
    dt = T / N  # Time step size

    # Use Adj Close if available; otherwise, use Close
    if "Adj Close" in data.columns:
        prices = data["Adj Close"]
    else:
        prices = data["Close"]

    S0 = prices.iloc[-1]  # Use the last available price

    # Compute log returns
    data["Log Returns"] = np.log(prices / prices.shift(1))

    # Calculate drift (mu) and volatility (sigma)
    mean_log_return = data["Log Returns"].mean()
    sigma = data["Log Returns"].std()
    mu = mean_log_return * 252 + 0.5 * sigma ** 2  # Annualized drift

    # Generate Brownian motion (Wiener process)
    np.random.seed(42)
    W = np.random.normal(0, np.sqrt(dt), size=N).cumsum()

    # Compute GBM stock price path
    t = np.linspace(0, T, N)
    S = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W)

    # Plot GBM simulation
    plt.figure(figsize=(10, 5))
    plt.plot(t, S, label="GBM Stock Price", color="blue")
    plt.xlabel("Time (Years)")
    plt.ylabel("Stock Price")
    plt.title(f"{ticker} Geometric Brownian Motion Simulation")
    plt.legend()

    save_path = os.path.join(save_dir, f"{ticker} Geometric Brownian Motion Simulation")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
