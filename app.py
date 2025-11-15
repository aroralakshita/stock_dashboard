import streamlit as st
import pandas as pd
from src.data_processing import load_csv, clean_numeric_columns, moving_avg
from src.viz import plot_closing_price_with_ma

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

df = load_csv(ticker)
df = clean_numeric_columns(df)

df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

df = moving_avg(df, windows=ma_options)

print(df.head())
print(df.info())
print(df.columns)

fig = plot_closing_price_with_ma(df)
st.plotly_chart(fig, use_container_width=True)

if st.checkbox("Show Raw Data"):
    st.dataframe(df)


