import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

st.set_page_config(page_title="Portfolio vs Benchmark Dashboard", layout="wide")

st.title("📊 Portfolio Performance Tracker")

# Upload Schwab file
uploaded_file = st.file_uploader("Upload Schwab Positions CSV", type="csv")

if uploaded_file:
    # Skip first 8 rows of metadata
    df = pd.read_csv(uploaded_file, skiprows=8)

    # Clean numeric columns (remove $, commas, %, and convert to float)
    def clean_numeric(col):
        return pd.to_numeric(col.replace({'[$,%()]': '', ',': ''}, regex=True), errors='coerce')

    df["Total Market Value"] = clean_numeric(df["Total Market Value"])
    portfolio_value = df["Total Market Value"].sum()

    st.subheader("💼 Current Portfolio Holdings")
    st.dataframe(df[["Symbol/CUSIP", "Name", "Quantity", "Price", "Total Market Value"]])

    st.metric("Total Portfolio Value", f"${portfolio_value:,.2f}")

    # Get benchmark data (e.g., SPY)
    st.subheader("📈 Performance vs. SPY")
    benchmark_symbol = st.text_input("Enter benchmark symbol (default: SPY)", value="SPY")

    start_date = datetime.date.today() - datetime.timedelta(days=30)
    end_date = datetime.date.today()

    benchmark_data = yf.download(benchmark_symbol, start=start_date, end=end_date)

    if not benchmark_data.empty:
        benchmark_data['Returns'] = benchmark_data['Adj Close'].pct_change().fillna(0)
        benchmark_data['Cumulative'] = (1 + benchmark_data['Returns']).cumprod()

        st.line_chart(benchmark_data['Cumulative'], height=300, use_container_width=True)
    else:
        st.warning("Could not retrieve benchmark data. Please check the symbol.")

else:
    st.info("Please upload your Schwab CSV file to begin.")
