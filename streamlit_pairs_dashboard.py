
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Load pair results
pair_df = pd.read_csv("all_pair_optimization_results.csv")
pair_df = pair_df.sort_values(by="Sharpe", ascending=False)

# Filters
min_sharpe = st.sidebar.slider("Min Sharpe Ratio", -5.0, 5.0, 0.0, 0.1)
min_trades = st.sidebar.slider("Min Number of Trades", 0, 300, 10, 5)
top_n = st.sidebar.slider("Show Top N Pairs", 1, 50, 10)

filtered = pair_df[(pair_df["Sharpe"] >= min_sharpe) & (pair_df["Trades"] >= min_trades)].head(top_n)
st.title("📈 Pairs Trading Dashboard")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

# Safe selectbox logic
if not filtered.empty:
    selected_row = st.selectbox("Select a pair to view backtest", filtered.index)

    if selected_row in filtered.index:
        row = filtered.loc[selected_row]
        stock1 = row["Stock 1"]
        stock2 = row["Stock 2"]
        hedge_ratio = None

        # Load price data
        data = pd.read_csv("price_data.csv", index_col=0, parse_dates=True)
        if stock1 in data.columns and stock2 in data.columns:
            s1 = data[stock1]
            s2 = data[stock2]

            # Estimate hedge ratio
            import statsmodels.api as sm
            X = sm.add_constant(s2)
            model = sm.OLS(s1, X).fit()
            hedge_ratio = model.params[stock2]

            spread = s1 - hedge_ratio * s2
            zscore = (spread - spread.rolling(30).mean()) / spread.rolling(30).std()

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread"))
            fig.add_trace(go.Scatter(x=spread.index, y=spread.rolling(30).mean(), name="Rolling Mean"))
            fig.add_trace(go.Scatter(x=spread.index, y=spread.rolling(30).mean() + zscore.std(), name="+1σ", line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=spread.index, y=spread.rolling(30).mean() - zscore.std(), name="-1σ", line=dict(dash='dot')))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            **Hedge Ratio**: {hedge_ratio:.3f}  
            **Pair**: `{stock1}` (long) vs `{stock2}` (short)  
            **Entry Z**: ±1.0 | **Exit Z**: 0.5
            """)
        else:
            st.error("Selected stocks not found in price data.")
    else:
        st.info("Please select a valid pair to display.")
else:
    st.warning("No pairs match your filters. Adjust the sliders.")
