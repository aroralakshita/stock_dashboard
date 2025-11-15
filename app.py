import streamlit as st
import pandas as pd
from src.data_processing import load_csv, clean_numeric_columns, moving_avg
from src.viz import plot_closing_price, plot_closing_price_with_ma, plot_volume_vs_return

st.sidebar.title("stock dashboard")

ticker = st.sidebar.selectbox("select stock", ["AAPL"])

st.write("DEBUG — ticker Streamlit received:", ticker)
print("DEBUG — ticker:", ticker)


ma_options = st.sidebar.multiselect(
    "Select Moving Averages",
    options=[20, 50],
    default=[20, 50]
)

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-11-16"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-11-14"))

show_closing_price_line = st.sidebar.checkbox("Show simple closing price", value=True)
show_ma_line = st.sidebar.checkbox("Show moving averages", value=True)
show_scatter = st.sidebar.checkbox("Show volume vs daily return", value=True)

df = load_csv(ticker)
df = clean_numeric_columns(df)

df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

if ma_options:
    df = moving_avg(df, windows=ma_options)

if show_closing_price_line:
    st.subheader("CLosing Price Over Time")
    fig1 = plot_closing_price(df)
    st.plotly_chart(fig1, use_container_width=True)

if show_ma_line:
    st.subheader("Closing Price with Moving Averages")
    fig2 = plot_closing_price_with_ma(df)
    st.plotly_chart(fig2, use_container_width=True)

if show_scatter:
    st.subheader("Volume vs Daily Return")
    fig3 = plot_volume_vs_return(df)
    st.plotly_chart(fig3, use_container_width=True)


print(df.head())
print(df.info())
print(df.columns)



if st.checkbox("Show Raw Data"):
    st.dataframe(df)


