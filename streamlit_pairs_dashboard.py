import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load precomputed optimization results
@st.cache_data
def load_data():
    df = pd.read_csv("all_pair_optimization_results.csv")
    return df

st.set_page_config(layout="wide")
st.title("📈 Pairs Trading Leaderboard")

# Load data
df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("Filter Options")
    min_sharpe = st.slider("Minimum Sharpe Ratio", -2.0, 5.0, 0.5, 0.1)
    max_trades = st.slider("Maximum Trades", 0, 500, 100, 10)
    top_n = st.slider("Top N Results", 5, 50, 10)

# Apply filters
filtered = df[(df['Sharpe'] >= min_sharpe) & (df['Trades'] <= max_trades)]
filtered = filtered.sort_values(by='Sharpe', ascending=False).head(top_n)

# Leaderboard table
st.subheader("🔝 Top Pairs by Sharpe Ratio")
st.dataframe(filtered, use_container_width=True)

# Plot selected pair's cumulative return
st.subheader("📊 Strategy Return Plot")
selected_row = st.selectbox("Select a row to visualize", filtered.index)
row = filtered.loc[selected_row]

# Load the price data again
data = pd.read_csv("price_data.csv", index_col=0, parse_dates=True)
s1 = data[row['Stock 1']]
s2 = data[row['Stock 2']]

# Recompute spread and return
import statsmodels.api as sm
X = sm.add_constant(s2)
model = sm.OLS(s1, X).fit()
hedge_ratio = model.params[row['Stock 2']]
spread = s1 - hedge_ratio * s2

spread_df = pd.DataFrame(index=spread.index)
spread_df['Spread'] = spread
spread_df['Mean'] = spread.rolling(int(row['Rolling Window'])).mean()
spread_df['Std'] = spread.rolling(int(row['Rolling Window'])).std()
spread_df['Z'] = (spread - spread_df['Mean']) / spread_df['Std']
spread_df = spread_df.dropna()

spread_df['Long'] = (spread_df['Z'] < -row['Entry Z']).astype(int)
spread_df['Short'] = (spread_df['Z'] > row['Entry Z']).astype(int)
spread_df['Exit'] = (spread_df['Z'].abs() < row['Exit Z']).astype(int)

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
spread_df.loc[spread_df['Trade'], 'PnL'] -= 0.002  # transaction cost
spread_df['Cumulative'] = (1 + spread_df['PnL']).cumprod()

fig = go.Figure()
fig.add_trace(go.Scatter(x=spread_df.index, y=spread_df['Cumulative'], mode='lines', name='Cumulative Return'))
fig.update_layout(title=f"{row['Stock 1']} vs {row['Stock 2']}", xaxis_title="Date", yaxis_title="Cumulative Return")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit • Author: Your Name • Data: Pairs Trading Optimizer")
