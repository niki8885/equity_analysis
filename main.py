import data_request
import charts

ticker = 'MSCI'

data_15m = data_request.request_data(ticker, "15m", start_days=1, save=True, filename="data_15m.csv")
data_1h = data_request.request_data(ticker, "1h", start_days=2, save=True, filename="data_1h.csv")
data_1d = data_request.request_data(ticker, "1d", start_days=30, save=True, filename="data_1d.csv")
data_1w = data_request.request_data(ticker, "1wk", start_days=180, save=True, filename="data_1w.csv")
data_1m = data_request.request_data(ticker, "1mo", start_days=365, save=True, filename="data_1m.csv")

basic_info = data_request.basic_analysis(ticker)

charts.candlestick_chart(data_15m, "15-Minute Candlestick Chart")
charts.lineplot_chart(data_15m, "15-Minute Line Chart")

charts.candlestick_chart(data_1h, "Hourly Candlestick Chart")
charts.lineplot_chart(data_1h, "Hourly Line Chart")

charts.candlestick_chart(data_1d, "Daily Candlestick Chart")
charts.lineplot_chart(data_1d, "Daily Line Chart")

charts.candlestick_chart(data_1w, "Weekly Candlestick Chart")
charts.lineplot_chart(data_1w, "Weekly Line Chart")

charts.candlestick_chart(data_1m, "Monthly Candlestick Chart")
charts.lineplot_chart(data_1m, "Monthly Line Chart")

