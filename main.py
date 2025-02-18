import equity_analysis as ea

ticker = 'MS'
# ea.clear_working_folders()
ea.all_data_request(ticker)
ea.request_fin_data(ticker)
ea.get_latest_fundamental(ticker)
ea.get_latest_stock_valuation(ticker)
current_price = ea.price(ticker,"current")
ea.add_analytics_to_df()
ea.generate_charts(ticker)
ea.plot_indicators()
ea.prediction_mcs()
ea.conf_intervals()
ea.probability_of_target (150)
ea.probability_distribution(current_price)
ea.risk_reward_analysis(current_price,150,110)
ea.stress_test_mcs()
ea.stress_test_mcs(stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=True)
ea.stress_test_mcs(stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=False)
ea.indices_corr("pearson", ticker)
ea.indices_corr("spearman", ticker)
ea.indices_corr("kendall", ticker)

# TODO: 📌 Dividend Metrics
# TODO: Dividend Yield
# TODO: Payout Ratio

# TODO: 📈 Company Valuation Methods
# TODO: Discounted Cash Flow (DCF)
# TODO: Comparable Company Analysis (CCA)
# TODO: Liquidation Value Assessment

# TODO: 🔥 Qualitative Analysis Factors
# TODO: Management Evaluation
# TODO: Market Conditions and Prospects
# TODO: SWOT Analysis
