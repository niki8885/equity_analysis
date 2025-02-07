import yfinance as yf
from datetime import datetime, timedelta


def get_date(days_ago):
    return (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')


today = get_date(0)


def basic_analysis(ticker):
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
    ticker = yf.Ticker(ticker)
    start = get_date(start_days)
    end = get_date(end_days)
    data = ticker.history(interval=interval, start=start, end=end)

    if save and filename:
        data.to_csv(f"./data/{filename}")

    return data
