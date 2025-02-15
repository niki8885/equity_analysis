import data_request, charts, vis_analytics, analytics, MCS

ticker = 'MS'

basic_info = data_request.basic_analysis(ticker)
data_15m,data_1h,data_1d,data_1w,data_1m = data_request.request_all_data(ticker)

vis_analytics.add_to_csv()
charts.generate_charts(data_15m,data_1h,data_1d,data_1w,data_1m)

forecast = MCS.prediction_mcs(data_1d)
median_price, lower_bound, upper_bound = MCS.conf_intervals(forecast)
prob = MCS.probability_of_target(forecast,595)
print(f'Probability of target = {prob} %')

last_price = data_1h["Close"].dropna().iloc[-1]
probability_df = MCS.probability_distribution(forecast,last_price)

take_profit = 585
stop_loss = 550
risk_reward_result = MCS.risk_reward_analysis(forecast, last_price, take_profit, stop_loss)

print(risk_reward_result)

historical_volatility = analytics.calculate_historical_volatility(data_1d)
stress_factor = 1.5  # Increase volatility by 50%
max_price_multiplier = 3  # Limit price growth to 3x the initial price
stressed_forecast_log = MCS.stress_test_mcs(forecast, historical_volatility, stress_factor, max_price_multiplier, use_log_normal=True)
stressed_forecast_norm = MCS.stress_test_mcs(forecast, historical_volatility, stress_factor, max_price_multiplier, use_log_normal=False)