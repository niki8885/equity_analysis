import data_request
import charts
import vis_analytics


ticker = 'MSCI'

basic_info = data_request.basic_analysis(ticker)
data_15m,data_1h,data_1d,data_1w,data_1m = data_request.request_all_data(ticker)

vis_analytics.add_to_csv()
charts.generate_charts(data_15m,data_1h,data_1d,data_1w,data_1m)


