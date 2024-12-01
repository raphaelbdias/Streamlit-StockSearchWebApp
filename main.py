import yfinance as yf
import numpy as np

# Define stock tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']  # Example tickers

# Initialize an empty list for scores
stock_scores = []

# Define weights for metrics
weights = {
    "pe": 0.3,
    "peg": 0.3,
    "roi": 0.2,
    "div_yield": 0.2
}

# Helper function: Normalize value to a 0-10 scale
def normalize(value, min_val, max_val):
    if value is None or np.isnan(value) or max_val <= min_val:
        return 0
    return (value - min_val) / (max_val - min_val) * 10

# Function to calculate ROI based on price change and dividends
def calculate_roi(stock):
    try:
        hist = stock.history(period="1y")  # Fetch 1 year of historical data
        price_start = hist['Close'][0]
        price_end = hist['Close'][-1]
        dividends = hist['Dividends'].sum()
        roi = ((price_end - price_start) + dividends) / price_start
        return roi
    except Exception:
        return np.nan

# Loop through each stock
for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Fetch and normalize metrics
    try:
        pe = normalize(info.get("trailingPE"), 0, 50)  # Normalize P/E ratio (0-50 range)
        peg = normalize(info.get("pegRatio"), 0, 2)   # Normalize PEG ratio (0-2 range)
        roi = normalize(calculate_roi(stock), -0.5, 0.5)  # ROI (assuming -50% to 50% range)
        div_yield = normalize(info.get("dividendYield", 0) * 100, 0, 10)  # Dividend Yield (0%-10% range)

        # Calculate composite score
        score = (
            weights["pe"] * pe +
            weights["peg"] * peg +
            weights["roi"] * roi +
            weights["div_yield"] * div_yield
        )
        stock_scores.append((ticker, score))
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# Calculate average portfolio score
average_score = np.mean([score for _, score in stock_scores])

# Print results
print("Stock Scores:")
for ticker, score in stock_scores:
    print(f"{ticker}: {score:.2f}")
print(f"\nAverage Portfolio Score: {average_score:.2f}")
