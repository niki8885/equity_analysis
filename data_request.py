import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import re


def get_date(days_ago):
    """Returns a date string (YYYY-MM-DD) for the given number of days ago."""
    return (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')


today = get_date(0)


def extract_timezone(datetime_str):
    """Extracts the timezone offset from a datetime string (e.g., '+04:00' or '-04:00')."""
    match = re.search(r'([-+]\d{2}:\d{2})$', str(datetime_str))
    return match.group(1) if match else None


def basic_analysis(ticker):
    """Fetches fundamental data for the given stock ticker."""
    ticker = yf.Ticker(ticker)
    return {
        "isin": ticker.isin,
        "info": ticker.info,
        "calendar": ticker.calendar,
        "dividends": ticker.dividends,
        "splits": ticker.splits,
        "capital_gains": ticker.capital_gains,
        "balance_sheets": ticker.balance_sheet,
        "cashflow": ticker.cashflow,
        "analysis": ticker.analyst_price_targets,
        "income": ticker.income_stmt,
        "quarterly_income": ticker.quarterly_income_stmt
    }


def request_data(ticker, interval, start_days, end_days=0, save=False, filename=None):
    """
    Fetches historical stock data for a given ticker, time interval, and date range.

    - `ticker`: Stock ticker symbol.
    - `interval`: Time interval ('15m', '1h', '1d', etc.).
    - `start_days`: Number of days ago for the start date.
    - `end_days`: Number of days ago for the end date (default: 0 for today).
    - `save`: Whether to save the data as a CSV file.
    - `filename`: Name of the CSV file (if `save` is True).
    """
    ticker = yf.Ticker(ticker)
    start = get_date(start_days)
    end = get_date(end_days)
    data = ticker.history(interval=interval, start=start, end=end)

    # Check the columns of the returned DataFrame
    print("Columns in data:", data.columns)

    # Reset index to move Date to a separate column (if it's set as index)
    data.reset_index(inplace=True)

    # Rename the column if it's not 'Date'
    if 'Datetime' in data.columns:
        data.rename(columns={'Datetime': 'Date'}, inplace=True)

    # Ensure the 'Date' column is in datetime format (check the actual column name)
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
    else:
        raise ValueError("No recognizable date column found in the data.")

    # Extract timezone information and store it in a separate column
    data['Timezone'] = data['Date'].apply(lambda x: x.tzinfo if x.tzinfo else None)

    # Remove timezone from the Date column
    data['Date'] = data['Date'].dt.tz_localize(None)

    # Optionally save the data to a CSV file
    if save and filename:
        data.to_csv(f"./data/{filename}", index=False)

    return data


def request_all_data(ticker):
    """
    Fetches stock data for multiple timeframes and saves them as CSV files.

    Returns data for:
    - 15-minute interval (1 day)
    - 1-hour interval (2 days)
    - 1-day interval (180 days)
    - 1-week interval (2 years)
    - 1-month interval (3 years)
    """
    data_15m = request_data(ticker, "15m", start_days=1, save=True, filename="data_15m.csv")
    data_1h = request_data(ticker, "1h", start_days=2, save=True, filename="data_1h.csv")
    data_1d = request_data(ticker, "1d", start_days=180, save=True, filename="data_1d.csv")
    data_1w = request_data(ticker, "1wk", start_days=730, save=True, filename="data_1w.csv")  # 2 years
    data_1m = request_data(ticker, "1mo", start_days=1095, save=True, filename="data_1m.csv")  # 3 years

    return data_15m, data_1h, data_1d, data_1w, data_1m

