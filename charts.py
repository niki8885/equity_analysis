import matplotlib.pyplot as plt
import vis_analytics
import mplfinance as mpf
import pandas as pd


def candlestick_chart(data, title="Candlestick Chart"):
    """Displays a candlestick chart."""
    if data is not None and not data.empty:
        # Ensure the index is a DatetimeIndex
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)

        # Plot the candlestick chart
        mpf.plot(data, type='candle', style='charles', title=title, volume=True)
    else:
        print("Not enough data to display the chart.")


def lineplot_chart(data, title="Line Chart", analytics='MA', period=50):
    """Displays a line chart of closing prices with an additional analytic."""
    if data is not None and not data.empty:
        plt.figure(figsize=(10, 5))

        # Plot closing price
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')

        # Calculate and plot the selected analytic (default is Moving Average)
        if analytics == 'MA':
            ma = vis_analytics.moving_average(data, period)
            plt.plot(data.index, ma, label=f'{period}-Day MA', color='red')

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


# TODO: Fix date handling and formatting in charts
# TODO: Add variability options for chart titles and grids
# TODO: Implement function selection for different types of visualizations