import os
import glob
import pandas as pd
from equity_analysis.utils import price


def load_csv(file_pattern):
    files = glob.glob(file_pattern)
    if not files:
        raise FileNotFoundError(
            f"No file matching {os.path.basename(file_pattern)} found in {os.path.dirname(file_pattern)}")
    return pd.read_csv(files[0])


def get_value(df, row_name, date):
    match = df[df.iloc[:, 0].str.contains(row_name, case=False, na=False)]
    return match[date].values[0] if not match.empty else 0


def fundamental(ticker,discount_rate = 0.1, years = 5,growth_rate = 0.05):
    df_income = load_csv(f"../data/financial_data/{ticker}_income.csv")
    df_balance = load_csv(f"../data/financial_data/{ticker}_balance_sheets.csv")
    df_financial = load_csv(f"../data/financial_data/{ticker}_financial.csv")
    df_cashflow= load_csv(f"../data/financial_data/{ticker}_cashflow.csv")

    dates = df_income.columns[1:]

    results = {}

    for date in dates:
        total_revenue = get_value(df_income, "Total Revenue", date)
        net_income = get_value(df_income, "Net Income Common Stockholders", date)
        tax_provision = get_value(df_income, "Tax Provision", date)
        reconciled_depreciation = get_value(df_income, "Reconciled Depreciation", date)
        interest_expense = get_value(df_income, "Interest Expense", date)
        total_liabilities = get_value(df_balance, "Total Liabilities Net Minority Interest", date)
        total_assets = get_value(df_balance, "Total Assets", date)
        shareholders_equity = get_value(df_balance, "Stockholders Equity", date)
        pretax_income = get_value(df_financial, "Pretax Income", date)
        fcf = get_value(df_cashflow, "Free Cash Flow", date)

        current_assets = sum(
            get_value(df_balance, name, date) for name in
            ["Cash And Cash Equivalents", "Receivables", "Investments And Advances", "Accounts Receivable"]
        )
        current_liabilities = sum(
            get_value(df_balance, name, date) for name in
            ["Current Debt And Capital Lease Obligation", "Payables And Accrued Expenses", "Accounts Payable"]
        )

        ebitda = net_income + interest_expense + reconciled_depreciation + tax_provision

        roe = net_income / shareholders_equity * 100 if shareholders_equity else 0
        roa = net_income / total_assets * 100 if total_assets else 0
        roic = (net_income * (1 - tax_provision / pretax_income)) / (
                    total_assets - total_liabilities) * 100 if pretax_income else 0
        current_ratio = current_assets / current_liabilities if current_liabilities else 0
        d_e = total_liabilities / shareholders_equity if shareholders_equity else 0
        int_cov_ratio = ebitda / interest_expense if interest_expense else 0
        asset_turnover_ratio = total_revenue / total_assets if total_assets else 0
        future_fcfs = [fcf * (1 + growth_rate) ** i for i in range(1, years + 1)]
        discounted_fcfs = [future_fcfs[i] / ((1 + discount_rate) ** (i + 1)) for i in range(years)]
        dcf_value = sum(discounted_fcfs)
        liquidation_value = total_assets - total_liabilities

        results[date] = {
            "Revenue": total_revenue,
            "Net Income": net_income,
            "EBITDA": ebitda,
            "Return on Equity (ROE)": roe,
            "Return on Assets (ROA)": roa,
            "Return on Invested Capital (ROIC)": roic,
            "Current Ratio": current_ratio,
            "Debt-to-Equity Ratio (D/E)": d_e,
            "Interest Coverage Ratio": int_cov_ratio,
            "Asset Turnover Ratio": asset_turnover_ratio,
            "Discounted Cash Flow": dcf_value,
            "Liquidation Value": liquidation_value
        }

    df_results = pd.DataFrame.from_dict(results, orient='index')

    output_dir = "../data/reports"
    output_path = os.path.join(output_dir, f"{ticker}_financial_report.csv")
    df_results.to_csv(output_path)

    return df_results


def get_latest_fundamental(ticker,discount_rate = 0.1, years = 5,growth_rate = 0.05):
    df = fundamental(ticker,discount_rate, years,growth_rate)
    latest_date = df.index[-1]
    latest_values = df.loc[latest_date]

    print(f"\nLatest Financial Metrics for {ticker} as of {latest_date}:\n")
    print(f"{'Metric':<35} {'Value'}")
    print("-" * 50)

    for metric, value in latest_values.items():
        print(f"{metric:<35} {value:,.2f}")

    return latest_values


def stock_valuation(ticker):
    df_income = load_csv(f"../data/financial_data/{ticker}_income.csv")
    df_balance = load_csv(f"../data/financial_data/{ticker}_balance_sheets.csv")
    df_info = load_csv(f"../data/financial_data/{ticker}_info.csv")

    dates = df_income.columns[1:]

    results = {}

    shares_outstanding = df_info["sharesOutstanding"].dropna().iloc[-1]
    market_cap = df_info["marketCap"].dropna().iloc[-1]
    current_price = price(ticker, method = "current")

    for date in dates:
        total_revenue = get_value(df_income, "Total Revenue", date)
        net_income = get_value(df_income, "Net Income Common Stockholders", date)
        tax_provision = get_value(df_income, "Tax Provision", date)
        reconciled_depreciation = get_value(df_income, "Reconciled Depreciation", date)
        interest_expense = get_value(df_income, "Interest Expense", date)
        shareholders_equity = get_value(df_balance, "Stockholders Equity", date)
        total_debt = get_value(df_balance, "Total Debt", date)
        cash = get_value(df_balance, "Cash And Cash Equivalents", date)

        eps = net_income / shares_outstanding if shares_outstanding else 0
        p_e = current_price / eps if eps else 0
        bvps = shareholders_equity / shares_outstanding if shares_outstanding else 0
        p_b = current_price / bvps if bvps else 0
        sps = total_revenue / shares_outstanding if shares_outstanding else 0
        p_s = current_price / sps if sps else 0
        ebitda = net_income + interest_expense + reconciled_depreciation + tax_provision
        ev = market_cap + total_debt - cash
        ev_ebitda = ev / ebitda if ebitda else 0
        ev_sales = ev / total_revenue if total_revenue else 0

        results[date] = {
            "P/E Ratio": p_e,
            "P/B Ratio": p_b,
            "P/S Ratio": p_s,
            "EV/EDITDA Ratio": ev_ebitda,
            "EV/Sales Ratio": ev_sales,
        }

    df_results = pd.DataFrame.from_dict(results, orient='index')

    output_dir = "../data/reports"
    output_path = os.path.join(output_dir, f"{ticker}_stock_valuation_report.csv")
    df_results.to_csv(output_path)

    return df_results


def get_latest_stock_valuation(ticker):
    df = stock_valuation(ticker)
    latest_date = df.index[-1]
    latest_values = df.loc[latest_date]

    print(f"\nLatest Stocks Metrics for {ticker} as of {latest_date}:\n")
    print(f"{'Metric':<35} {'Value'}")
    print("-" * 50)

    for metric, value in latest_values.items():
        print(f"{metric:<35} {value:,.2f}")

    return latest_values


def get_dividend_metrics(ticker):
    # Load financial data
    df_info = load_csv(f"../data/financial_data/{ticker}_info.csv")
    current_price = price(ticker, method="current")

    # Extract and handle missing data
    payout_ratio = df_info["payoutRatio"].dropna().iloc[-1] if not df_info["payoutRatio"].dropna().empty else None
    div_rate = df_info["dividendRate"].dropna().iloc[-1] if not df_info["dividendRate"].dropna().empty else None
    dividend_yield = (div_rate / current_price) * 100 if div_rate and current_price else None

    # Store results in a dictionary
    metrics = {
        "Dividend Yield (%)": dividend_yield,
        "Payout Ratio": payout_ratio
    }

    # Print formatted output
    print("\nDividend Metrics for", ticker)
    print("-" * 40)
    print(f"Dividend Yield (%): {metrics['Dividend Yield (%)']:.2f}%" if metrics["Dividend Yield (%)"] is not None else "Dividend Yield: N/A")
    print(f"Payout Ratio: {metrics['Payout Ratio']:.2f}" if metrics["Payout Ratio"] is not None else "Payout Ratio: N/A")
    print("-" * 40)

    # Convert to DataFrame and save as CSV
    df_results = pd.DataFrame(metrics, index=[0])  # Convert dictionary to DataFrame properly

    output_dir = "../data/reports"
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
    output_path = os.path.join(output_dir, f"{ticker}_dividend_metrics_report.csv")

    df_results.to_csv(output_path, index=False)  # Save without index

    return metrics
