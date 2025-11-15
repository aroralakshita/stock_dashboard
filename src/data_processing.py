import yfinance as yf
import pandas as pd

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#def fetch_stock(ticker, start_date, end_date):
 # ticker → stock symbol (e.g., "AAPL" for Apple)
    
   #stock = yf.Ticker(ticker)
   #df = stock.history(start=start_date, end=end_date)
    
   #if df.empty:
      #raise ValueError(f"No data returned for {ticker}. Try again in 30–60 seconds.")


def load_csv(ticker: str):
    path = os.path.join(BASE_DIR, "data", f"{ticker}.csv")
    print("Loading:", path)
    df = pd.read_csv(path)
    df = df.reset_index()
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])

    return df


def clean_numeric_columns(df):

   df = df.rename(columns={"close/last": "close"})

   price_cols = ["close", "open", "high", "low"]
   for col in price_cols:
      df[col] = df[col].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

   return df

def moving_avg(df, windows=[20, 50]):
   for w in windows:
      col_name = f"ma_{w}"
      df[col_name] = df["close"].rolling(window=w).mean()
   return df

if __name__ == "__main__":
    print("TEST: data_processing.py is running")
    df = load_csv("AAPL")
    print(df.head())