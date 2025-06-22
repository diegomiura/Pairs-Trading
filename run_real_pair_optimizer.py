
import yfinance as yf
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from itertools import combinations
import numpy as np

# Download real adjusted close prices
tickers = ["V", "MA", "MSFT", "AAPL", "JPM", "BAC"]
start = "2020-01-01"
end = "2024-12-31"
data = yf.download(tickers, start=start, end=end)["Close"]
data = data.dropna()
data.to_csv("price_data.csv")

# Optimize pairs
results = []

for stock1, stock2 in combinations(tickers, 2):
    s1 = data[stock1]
    s2 = data[stock2]

    score, pvalue, _ = coint(s1, s2)
    if pvalue > 0.05:
        continue  # skip non-cointegrated

    # Estimate hedge ratio
    X = sm.add_constant(s2)
    model = sm.OLS(s1, X).fit()
    hedge_ratio = model.params[stock2]
    spread = s1 - hedge_ratio * s2

    spread_df = pd.DataFrame(index=spread.index)
    spread_df['Spread'] = spread
    spread_df['Mean'] = spread.rolling(30).mean()
    spread_df['Std'] = spread.rolling(30).std()
    spread_df['Z'] = (spread - spread_df['Mean']) / spread_df['Std']
    spread_df = spread_df.dropna()

    spread_df['Long'] = (spread_df['Z'] < -1.0).astype(int)
    spread_df['Short'] = (spread_df['Z'] > 1.0).astype(int)
    spread_df['Exit'] = (spread_df['Z'].abs() < 0.5).astype(int)

    position = 0
    positions = []
    for i in range(len(spread_df)):
        if spread_df['Long'].iloc[i]:
            position = 1
        elif spread_df['Short'].iloc[i]:
            position = -1
        elif spread_df['Exit'].iloc[i]:
            position = 0
        positions.append(position)
    spread_df['Position'] = positions

    returns = pd.concat([s1, s2], axis=1).pct_change().dropna()
    returns.columns = ['ret1', 'ret2']
    common_index = spread_df.index.intersection(returns.index)
    spread_df = spread_df.loc[common_index]
    returns = returns.loc[common_index]

    spread_df['PnL'] = spread_df['Position'] * (returns['ret1'] - hedge_ratio * returns['ret2'])
    spread_df['Trade'] = spread_df['Position'].diff().abs() > 0
    spread_df.loc[spread_df['Trade'], 'PnL'] -= 0.002
    spread_df['Cumulative'] = (1 + spread_df['PnL']).cumprod()

    total_return = spread_df['Cumulative'].iloc[-1] - 1
    sharpe = spread_df['PnL'].mean() / spread_df['PnL'].std() * np.sqrt(252)
    trades = spread_df['Trade'].sum()

    results.append({
        "Stock 1": stock1,
        "Stock 2": stock2,
        "Rolling Window": 30,
        "Entry Z": 1.0,
        "Exit Z": 0.5,
        "Total Return": round(total_return * 100, 2),
        "Sharpe": round(sharpe, 2),
        "Trades": int(trades),
        "Cointegration p-value": round(pvalue, 4)
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Sharpe", ascending=False)
results_df.to_csv("all_pair_optimization_results.csv", index=False)
print("✅ Saved real optimization results to all_pair_optimization_results.csv")
