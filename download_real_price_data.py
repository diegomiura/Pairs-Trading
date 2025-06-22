
import yfinance as yf
import pandas as pd

# Choose your tickers and date range
tickers = ["V", "MA", "MSFT", "AAPL", "JPM", "BAC"]
start_date = "2020-01-01"
end_date = "2024-12-31"

# Download adjusted close prices
data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

# Drop rows with missing values
data = data.dropna()

# Save to CSV
data.to_csv("price_data.csv")
print("✅ Saved to price_data.csv")
