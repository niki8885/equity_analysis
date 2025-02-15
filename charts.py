import matplotlib.pyplot as plt
import vis_analytics
import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mdates


def candlestick_chart(data, title="Candlestick Chart"):
    """Displays a candlestick chart with correct date formatting."""
    if data is not None and not data.empty:
        # Ensure the Date column is in datetime format and set as index
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

        # Plot the candlestick chart
        mpf.plot(data, type='candle', style='charles', title=title, volume=True)
    else:
        print("Not enough data to display the chart.")

def lineplot_chart(data, title="Line Chart", analytics='MA', period=50):
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
        plt.grid()
        plt.show()
    else:
        print("Not enough data to display the chart.")


def generate_charts(data_15m, data_1h, data_1d, data_1w, data_1m):
    """Generates candlestick and line charts for different time intervals."""
    candlestick_chart(data_15m, "15-Minute Candlestick Chart")
    lineplot_chart(data_15m, "15-Minute Line Chart")

    candlestick_chart(data_1h, "Hourly Candlestick Chart")
    lineplot_chart(data_1h, "Hourly Line Chart")

    candlestick_chart(data_1d, "Daily Candlestick Chart")
    lineplot_chart(data_1d, "Daily Line Chart")

    candlestick_chart(data_1w, "Weekly Candlestick Chart")
    lineplot_chart(data_1w, "Weekly Line Chart")

    candlestick_chart(data_1m, "Monthly Candlestick Chart")
    lineplot_chart(data_1m, "Monthly Line Chart")


# TODO: Add variability options for chart titles and grids
# TODO: Implement function selection for different types of visualizations