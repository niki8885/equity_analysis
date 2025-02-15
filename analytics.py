import numpy as np

def calculate_historical_volatility(data):
    """
    Calculate annualized historical volatility from existing dataset.

    Arguments:
    - data: DataFrame containing historical price data with a 'Close' column.

    Returns:
    - Annualized historical volatility.
    """
    # Calculate daily log returns
    data["Log_Returns"] = np.log(data["Close"] / data["Close"].shift(1))

    # Compute standard deviation of daily returns (ignoring NaN values)
    daily_volatility = data["Log_Returns"].std()

    # Annualized volatility (assuming 252 trading days per year)
    annualized_volatility = daily_volatility * np.sqrt(252)

    return annualized_volatility



