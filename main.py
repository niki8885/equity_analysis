import equity_analysis as ea

ticker = 'MS'
ea.clear_working_folders()
ea.all_data_request(ticker)
ea.indices_corr("pearson", ticker)
ea.indices_corr("spearman", ticker)
ea.indices_corr("kendall", ticker)
ea.add_analytics_to_df()
ea.generate_charts(ticker)
ea.prediction_mcs()
ea.conf_intervals()
ea.probability_of_target (150)
ea.probability_distribution(139)
ea.risk_reward_analysis(139,150,110)
ea.stress_test_mcs()
ea.stress_test_mcs(stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=True)
ea.stress_test_mcs(stress_factor = 1.5, max_price_multiplier = 3, use_log_normal=False)

# last_price = data_1h["Close"].dropna().iloc[-1]
