import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
import os

save_dir = "../data/plots"


def prepare_indices(ticker):
    data = pd.read_csv("../data/raw_data/merged_indices.csv")
    rename_dict = {
        "Date": "Date",
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "Dow Jones",
        "^RUT": "Russell 2000",
        "^GDAXI": "DAX",
        "^FTSE": "FTSE 100",
        "^FCHI": "CAC 40",
        "^HSI": "Hang Seng",
        "^N225": "Nikkei 225",
        "^BSESN": "Sensex",
        "^BVSP": "Bovespa",
        "data_1d": ticker
    }

    data.rename(columns=rename_dict, inplace=True)

    processed_file_path = "../data/raw_data/merged_indices.csv"
    data.to_csv(processed_file_path, index=False)

    return data


def normalize_indices(data, type):
    """
    Normalizes index data based on the given method.
    """
    if type == "min_max":
        scaler = MinMaxScaler()
        data.iloc[:, 1:] = scaler.fit_transform(data.iloc[:, 1:])
    elif type == "z_score":
        scaler = StandardScaler()
        data.iloc[:, 1:] = scaler.fit_transform(data.iloc[:, 1:])
    elif type == "pct_change":
        data.iloc[:, 1:] = data.iloc[:, 1:].pct_change().fillna(0)
    else:
        raise ValueError("Unsupported normalization type")
    return data


def indices_corr(method, ticker_name):
    """
    Computes the correlation matrix of the indices and a given stock.
    """
    data = prepare_indices(ticker_name)
    if method == "pearson":
        data = normalize_indices(data, "pct_change")

    # Remove 'Date' column before correlation calculation
    numeric_data = data.drop(columns=['Date'])

    if method == "pearson":
        corr_matrix = numeric_data.corr(method="pearson")
    elif method == "spearman":
        corr_matrix = numeric_data.corr(method="spearman")
    elif method == "kendall":
        corr_matrix = numeric_data.corr(method="kendall")
    else:
        raise ValueError("Unsupported correlation method")

    # Find the indices with highest correlation
    best_corr_indices = corr_matrix[ticker_name].drop(ticker_name).nlargest(3)
    best_corr_str = ", ".join([f"{idx} ({corr:.2f})" for idx, corr in best_corr_indices.items()])

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title(f"{method.capitalize()} Correlation Matrix of {ticker_name}\nBest correlated: {best_corr_str}")
    save_path = os.path.join(save_dir, f"Correlation_Matrix_of_{ticker_name}_method_{method}.png")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
    print(f"Chart saved: {save_path}")
    # Plot line chart for best correlated indices
    plt.figure(figsize=(12, 6))
    for idx in best_corr_indices.index:
        plt.plot(data['Date'], data[idx], label=idx)
    plt.plot(data['Date'], data[ticker_name], label=ticker_name, linewidth=2, linestyle='dashed')
    plt.legend()
    plt.title(f"Price Trends of {ticker_name} and Top Correlated Indices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    save_path = os.path.join(save_dir, f"Price_Trends_of_{ticker_name}_and_Top_Correlated_Indices_method_{method}.png")
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
    print(f"Chart saved: {save_path}")
    return corr_matrix

# TODO: Implement function for optimize and choose best normalization method