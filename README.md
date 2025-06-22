
# 📊 Pairs Trading Dashboard

This project is a Streamlit-powered dashboard for testing and visualizing pairs trading strategies using real historical stock data.

---

## 🚀 Features

- Automatically selects cointegrated stock pairs using the Engle-Granger test
- Optimizes signal thresholds and lookbacks for Sharpe Ratio
- Visualizes signals, spread, and cumulative returns
- Built-in backtesting engine
- Fully interactive via web browser

---

## 🧰 Tech Stack

- Python 3.10 (required)
- Streamlit
- yfinance
- pandas, statsmodels, plotly

---

## 📦 Setup Locally

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/pairs-trading.git
cd pairs-trading
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run streamlit_pairs_dashboard.py
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push the repo to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"New App"**
4. Select:
   - Your GitHub repo
   - `streamlit_pairs_dashboard.py` as the main file
5. Under **Advanced Settings**, set the **Python version to 3.10**
6. Click **Deploy**

---

## 📝 Notes

- You **must** use Python 3.10. `statsmodels` is not compatible with Python 3.13+ as of June 2025.
- No `.streamlit/config.toml` is needed if you set the version manually in the Streamlit UI.
- The dashboard defaults to showing top 10 cointegrated pairs and lets you choose which to simulate.

---

## 📈 Sample Output

- Total return
- Sharpe Ratio
- Max drawdown
- Number of trades

---

## 📬 Questions?

Open an issue or reach out at diegomiura@example.com (replace with your contact).
