import matplotlib.pyplot as plt
import vis_analytics
import mplfinance as mpf

def candlestick_chart(data, title="Candlestick Chart"):
    """Displays a candlestick chart."""
    if data is not None and not data.empty:
        mpf.plot(data, type='candle', style='charles', title=title, volume=True)
    else:
        print("Not enough data to display the chart.")

def lineplot_chart(data, title="Line Chart"):
    """Displays a line chart of closing prices."""
    if data is not None and not data.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title(title)
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("Not enough data to display the chart.")
