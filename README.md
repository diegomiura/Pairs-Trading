# 📈 Pairs Trading Dashboard

An interactive Streamlit app for visualizing and evaluating cointegrated pairs trading strategies. It includes:

- A Sharpe-ranked leaderboard of optimized pairs
- A dynamic backtest plot of strategy performance
- Filters for Sharpe ratio, number of trades, and more
- Synthetic or real stock price data support

---

## 📁 Contents

| File | Purpose |
|------|---------|
| `streamlit_pairs_dashboard.py` | Main Streamlit dashboard app |
| `all_pair_optimization_results.csv` | Optimized pair backtest results |
| `price_data.csv` | Historical adjusted close prices (synthetic or real) |
| `download_real_price_data.py` | Script to fetch real price data via `yfinance` |
| `requirements.txt` | Python dependencies |

---

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/pairs-trading-dashboard.git
cd pairs-trading-dashboard
```

> 🔁 Replace `YOUR_USERNAME` with your actual GitHub username.

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. (Optional) Fetch Real Price Data

```bash
python download_real_price_data.py
```

---

### 4. Launch the Dashboard

```bash
streamlit run streamlit_pairs_dashboard.py
```

---

## 📌 Notes

- The dashboard works out-of-the-box using included synthetic data.
- To run real backtests, replace both `price_data.csv` and `all_pair_optimization_results.csv` with your own data.
- Optimizer code and clustering scripts can be added to extend the pipeline.

---

## ✍️ Author

Developed by [Your Name].  
Powered by Python, Streamlit, Pandas, and Plotly.
