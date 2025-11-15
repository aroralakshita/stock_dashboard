import yfinance as yf
import pandas as pd

def fetch_stock(ticker, start_date, end_date):
 # ticker → stock symbol (e.g., "AAPL" for Apple)
    
   stock = yf.Ticker(ticker)
   df = stock.history(start=start_date, end=end_date)
    
   if df.empty:
      raise ValueError(f"No data returned for {ticker}. Try again in 30–60 seconds.")

   df = df.reset_index()
   df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]

   return df

def clean_numeric_columns(df):

   price_cols = ["close/last", "open", "high", "low"]
   for col in price_cols:
      df[col] = df[col].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)
      df = df.rename(columns={"close/last": "close"})

   return df

def moving_avg(df, windows=[20, 50]):
   for w in windows:
      col_name = f"ma_{w}"
      df[col_name] = df["close"].rolling(window=w).mean()
   return df
