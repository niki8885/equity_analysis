import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mdates
import os

save_dir = "../data/plots"


def candlestick_chart(data, title="Candlestick Chart"):
    """Displays a candlestick chart and saves it to a file."""
    if data is not None and not data.empty:
        # Ensure the 'Date' column is in datetime format and set as index
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

        # Define the save path
        save_path = os.path.join(save_dir, f"{title}.png")

        # Plot and save the candlestick chart
        mpf.plot(data, type='candle', style='charles', title=title, volume=True, savefig=save_path)

        print(f"Chart saved: {save_path}")
    else:
        print("Not enough data to display the chart.")


def lineplot_chart(data, title="Line Chart"):
    """Displays a line chart of closing prices with an additional analytic."""
    if data is not None and not data.empty:
        # Ensure the Date column is in datetime format and set as index
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

        plt.figure(figsize=(10, 5))

        # Plot closing price
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')

        # Fix x-axis date format
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()

        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        save_path = os.path.join(save_dir, f"{title}.png")
        plt.savefig(save_path, dpi=600, bbox_inches='tight')
        print(f"Chart saved: {save_path}")
    else:
        print("Not enough data to display the chart.")


def generate_charts(ticker_name):
    """Generates candlestick and line charts for different time intervals."""
    timeframes = (" 15-Minute", " Hourly", " Daily", " Weekly", " Monthly")
    chart_types = (" Candlestick Chart", " Line Chart")
    data_15m = pd.read_csv("../data/raw_data/data_15m.csv")
    data_1h = pd.read_csv("../data/raw_data/data_1h.csv")
    data_1d = pd.read_csv("../data/raw_data/data_1d.csv")
    data_1w = pd.read_csv("../data/raw_data/data_1w.csv")
    data_1m = pd.read_csv("../data/raw_data/data_1m.csv")
    # Generate charts for all timeframes
    datasets = [data_15m, data_1h, data_1d, data_1w, data_1m]

    for i, data in enumerate(datasets):
        candlestick_chart(data, ticker_name + timeframes[i] + chart_types[0])
        lineplot_chart(data, ticker_name + timeframes[i] + chart_types[1])

# TODO: Implement function selection for different types of visualizations