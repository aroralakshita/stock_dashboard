import streamlit as st
import pandas as pd
from src.data_processing import load_stock_data, get_stock_data, clean_numeric_columns, moving_avg, bollinger_bands, compute_rsi, compute_macd, daily_return
from src.viz import plot_closing_price, plot_closing_price_with_ma, plot_volume_vs_return, plot_candlestick_with_bbands, plot_rsi, plot_macd, plot_multi_stock_comparison

st.sidebar.title("stock dashboard")

@st.cache_data
def load_all_stocks():
    return load_stock_data(['AAPL', 'TSLA', 'MSFT'], data_folder='data')

df_all = load_all_stocks()

# Stock selector
available_stocks = sorted(df_all['symbol'].unique())
ticker = st.sidebar.selectbox("Select Stock", available_stocks)

ma_options = st.sidebar.multiselect(
    "Select Moving Averages",
    options=[20, 50],
    default=[20, 50]
)

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-11-24"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-11-21"))

show_closing_price_line = st.sidebar.checkbox("Show simple closing price", value=True)
show_ma_line = st.sidebar.checkbox("Show moving averages", value=True)
show_scatter = st.sidebar.checkbox("Show volume vs daily return", value=True)
show_gainers_losers = st.sidebar.checkbox("Show top gainers/losers", value=True)
show_candles = st.sidebar.checkbox("Show Candlestick + Bollinger Bands", value=True)
show_rsi = st.sidebar.checkbox("Show RSI indicator", value=True)
show_macd = st.sidebar.checkbox("Show MACD inidcator", value=True)
show_comparison = st.sidebar.checkbox("Show multi-stock comparison", value=False)

df = get_stock_data(df_all, ticker)
df = clean_numeric_columns(df)
df = daily_return(df)

df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

df = bollinger_bands(df)

df = compute_rsi(df)
df = compute_macd(df)



tab1, tab2 = st.tabs(["Price Overwiew", "Technical Indicators"])

if ma_options:
    df = moving_avg(df, windows=ma_options)

if show_comparison:
    st.subheader("📊 Multi-Stock Comparison")
    comparison_stocks = st.multiselect(
        "Select stocks to compare",
        options=available_stocks,
        default=available_stocks[:3]
    )
    if comparison_stocks:
        # Filter date range for all stocks
        df_comparison = df_all[
            (df_all["date"] >= pd.to_datetime(start_date)) & 
            (df_all["date"] <= pd.to_datetime(end_date))
        ]
        fig_comp = plot_multi_stock_comparison(df_comparison, comparison_stocks)
        st.plotly_chart(fig_comp, use_container_width=True)

with tab1:
    if show_closing_price_line:
        st.subheader("CLosing Price Over Time")
        fig1 = plot_closing_price(df, symbol=ticker)
        st.plotly_chart(fig1, use_container_width=True)

    if show_candles:
        st.subheader("Candlestick + Bollinger Bands")
        fig4 = plot_candlestick_with_bbands(df, symbol=ticker)
        st.plotly_chart(fig4, use_container_width=True)

    if show_scatter:
        st.subheader("Volume vs Daily Return")
        fig3 = plot_volume_vs_return(df, symbol=ticker)
        st.plotly_chart(fig3, use_container_width=True)


with tab2:
    if show_ma_line:
        st.subheader("Closing Price with Moving Averages")
        fig2 = plot_closing_price_with_ma(df, symbol=ticker)
        st.plotly_chart(fig2, use_container_width=True)
    
    if show_rsi:
        st.subheader("RSI indicator")
        fig5 = plot_rsi(df, symbol=ticker)
        st.plotly_chart(fig5, use_container_width=True)
    
    if show_macd:
        st.subheader("MACD indicator")
        fig6 = plot_macd(df, symbol=ticker)
        st.plotly_chart(fig6, use_container_width=True)


print(df.head())
print(df.info())
print(df.columns)


if st.checkbox("Show Raw Data"):
    st.dataframe(df)


