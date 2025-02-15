import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


def prediction_mcs(data, days=30, simulations=1000):
    """
    Monte Carlo method for stock price forecasting.

    Arguments:
    - data: DataFrame with historical stock data, must contain the 'Close' column.
    - days: Number of days for the forecast.
    - simulations: Number of Monte Carlo simulations.

    Returns:
    - DataFrame with simulated price trajectories.
    """
    # Extract closing prices
    close_prices = data['Close'].dropna().values

    # Calculate logarithmic returns
    log_returns = np.log(close_prices[1:] / close_prices[:-1])

    # Compute model parameters
    mu = np.mean(log_returns)  # Expected return (drift)
    sigma = np.std(log_returns)  # Volatility

    # Initial price (last available price)
    S0 = close_prices[-1]

    # Array to store all simulations
    simulations_results = np.zeros((days, simulations))

    # Generate random price paths using the Monte Carlo method
    for i in range(simulations):
        # Generate random normal values Z
        Z = np.random.normal(0, 1, days)

        # Generate future logarithmic returns
        future_returns = mu - 0.5 * sigma ** 2 + sigma * Z

        # Generate the price trajectory
        price_path = S0 * np.exp(np.cumsum(future_returns))
        simulations_results[:, i] = price_path

    # Create a DataFrame with simulated price trajectories
    forecast_df = pd.DataFrame(simulations_results)

    return forecast_df


def conf_intervals(forecast):
    # Compute confidence intervals
    median_forecast = forecast.median(axis=1)  # 50th percentile (median)
    percentile_5 = forecast.quantile(0.05, axis=1)  # 5th percentile (worst-case scenario)
    percentile_95 = forecast.quantile(0.95, axis=1)  # 95th percentile (best-case scenario)

    # Convert index to numerical values for plotting
    x_values = np.arange(len(median_forecast))

    # Convert Series to NumPy arrays for plotting
    median_forecast = median_forecast.values
    percentile_5 = percentile_5.values
    percentile_95 = percentile_95.values

    # Visualization with confidence intervals
    plt.figure(figsize=(12, 6))
    plt.plot(x_values, median_forecast, label="Median Forecast", color="blue")
    plt.fill_between(x_values, percentile_5, percentile_95, color='blue', alpha=0.2, label="90% Confidence Interval")
    plt.title("Monte Carlo Price Forecast with Confidence Intervals")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Display forecasted values for the last day
    median_price = median_forecast[-1]
    lower_bound = percentile_5[-1]
    upper_bound = percentile_95[-1]

    return median_price, lower_bound, upper_bound


def probability_of_target(forecast, target_price):
    """
    Calculate the probability of the price reaching or exceeding a target level.

    Arguments:
    - forecast: DataFrame containing Monte Carlo simulated price paths.
    - target_price: The target price level (Take-Profit or Stop-Loss).

    Returns:
    - Probability (percentage) of reaching the target price within the forecast period.
    """
    # Count how many simulations reach or exceed the target price at any point
    simulations_reaching_target = (forecast >= target_price).any(axis=0).sum()

    # Compute probability as a percentage
    probability = (simulations_reaching_target / forecast.shape[1]) * 100

    return probability

def probability_distribution(forecast, current_price):
    """
    Calculate the probability of the price reaching different target levels.

    Arguments:
    - forecast: DataFrame containing Monte Carlo simulated price paths.
    - current_price: The current price of the asset.

    Returns:
    - DataFrame with target price levels and their probabilities.
    - Plot showing probability distribution for different targets.
    """
    target_prices = []  # List to store target price levels
    probabilities = []  # List to store corresponding probabilities

    # Generate target prices in the range of 75% to 125% of current price (increments of 5%)
    for multiplier in np.arange(1, 1.51, 0.05):  # Adjusted range to include 1.25
        price = current_price * multiplier
        target_prices.append(price)
        probability = probability_of_target(forecast, price)
        probabilities.append(probability)

    # Create a DataFrame with results
    probability_df = pd.DataFrame({
        "Target Price": target_prices,
        "Probability (%)": probabilities
    })

    # Plot the probability distribution
    plt.figure(figsize=(10, 5))
    plt.plot(probability_df["Target Price"], probability_df["Probability (%)"], marker="o", linestyle="-", color="blue")
    plt.xlabel("Target Price")
    plt.ylabel("Probability (%)")
    plt.title("Probability of Reaching Target Prices")
    plt.grid(True)
    plt.show()

    return probability_df


def risk_reward_analysis(forecast, current_price, take_profit, stop_loss):
    """
    Calculate the probability of hitting Take-Profit and Stop-Loss levels and assess the Risk/Reward Ratio.

    Arguments:
    - forecast: DataFrame containing Monte Carlo simulated price paths.
    - current_price: The current price of the asset.
    - take_profit: Target price level (profit goal).
    - stop_loss: Stop-loss level (maximum acceptable loss).

    Returns:
    - Dictionary with probabilities of hitting Take-Profit and Stop-Loss, and Risk/Reward Ratio.
    """
    # Calculate probabilities
    prob_take_profit = probability_of_target(forecast, take_profit)
    prob_stop_loss = probability_of_target(forecast, stop_loss)

    # Calculate potential reward and risk
    potential_reward = take_profit - current_price
    potential_risk = current_price - stop_loss

    # Avoid division by zero
    if potential_risk == 0:
        risk_reward_ratio = float('inf')  # Infinite if no risk
    else:
        risk_reward_ratio = potential_reward / potential_risk

    # Create result dictionary
    result = {
        "Take-Profit Probability (%)": round(float(prob_take_profit), 2),
        "Stop-Loss Probability (%)": round(float(prob_stop_loss), 2),
        "Risk/Reward Ratio": round(float(risk_reward_ratio), 2)
    }

    return result


def stress_test_mcs(forecast, sigma, stress_factor=1.5, max_price_multiplier=3, use_log_normal=True):
    """
    Perform stress testing by increasing volatility (σ) and assessing the impact on price distribution.
    Uses either a normal or log-normal distribution.
    Displays median forecast and confidence intervals instead of excessive trajectories.

    Arguments:
    - forecast: DataFrame containing Monte Carlo simulated price paths.
    - sigma: Historical volatility of the asset.
    - stress_factor: Multiplier to artificially increase volatility (default is 1.5x).
    - max_price_multiplier: Maximum multiple of the initial price to prevent unrealistic growth (default is 3x).
    - use_log_normal: If True, uses a log-normal distribution; otherwise, uses a normal distribution.

    Returns:
    - DataFrame with stressed simulation results.
    - Visualization of the impact on price projections with median and confidence intervals.
    """
    # Increase volatility by the stress factor
    stressed_sigma = min(sigma * stress_factor, 0.5)  # Limit max volatility to 50%

    # Extract the last observed price as the starting point
    S0 = forecast.iloc[0, 0]

    # Generate stressed Monte Carlo simulations
    days, simulations = forecast.shape
    stressed_results = np.zeros((days, simulations))

    for i in range(simulations):
        if use_log_normal:
            # Generate random values from a truncated normal distribution (log-normal approach)
            Z = stats.truncnorm.rvs(-2, 2, loc=0, scale=1, size=days)  # Clamped between -2σ and +2σ
        else:
            # Generate random values from a standard normal distribution
            Z = np.random.normal(0, 1, days)

        # Apply price path formula
        future_returns = -0.5 * stressed_sigma ** 2 + stressed_sigma * Z
        price_path = S0 * np.exp(np.cumsum(future_returns))

        # Limit excessive price growth to max_price_multiplier * S0
        price_path[price_path > S0 * max_price_multiplier] = S0 * max_price_multiplier

        stressed_results[:, i] = price_path

    # Create a DataFrame with stressed simulations
    stressed_forecast = pd.DataFrame(stressed_results)

    # Calculate median forecast and confidence intervals
    median_forecast = stressed_forecast.median(axis=1)
    percentile_5 = stressed_forecast.quantile(0.05, axis=1)
    percentile_95 = stressed_forecast.quantile(0.95, axis=1)

    # Ensure no NaN or infinite values
    percentile_5 = np.nan_to_num(percentile_5, nan=np.nanmin(percentile_5), posinf=np.nanmax(percentile_5),
                                 neginf=np.nanmin(percentile_5))
    percentile_95 = np.nan_to_num(percentile_95, nan=np.nanmax(percentile_95), posinf=np.nanmax(percentile_95),
                                  neginf=np.nanmin(percentile_95))
    median_forecast = np.nan_to_num(median_forecast, nan=np.nanmedian(median_forecast),
                                    posinf=np.nanmax(median_forecast), neginf=np.nanmin(median_forecast))

    # Visualization: Show median and confidence intervals instead of chaotic lines
    plt.figure(figsize=(12, 6))
    plt.plot(median_forecast, label="Median Forecast", color="black", linewidth=2)
    plt.fill_between(range(len(median_forecast)), percentile_5, percentile_95, color="red", alpha=0.2,
                     label="90% Confidence Interval")

    dist_type = "Log-Normal" if use_log_normal else "Normal"
    plt.title(f"Stress Test: Monte Carlo Price Forecast with {stress_factor}x Volatility ({dist_type} Distribution)")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

    return stressed_forecast
