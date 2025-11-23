import yfinance as yf
import pandas as pd
import streamlit as st

#import os
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def fetch_stock(ticker, start="2015-01-01", end=None):
 # ticker → stock symbol (e.g., "AAPL" for Apple)
    
   #stock = yf.Ticker(ticker)
   df = yf.download(ticker, start=start, end=end)
   df.reset_index(inplace=True)
   
   if isinstance(df.columns, pd.MultiIndex):
      df.columns = [c[0].lower() for c in df.columns]
   else:
      df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
   
   expected = ["date", "open", "high", "low", "close", "volume"]

   for c in expected:
      if c not in df.columns:
         raise KeyError(f"missing required column: {c}")
   
   return df[expected]
   #if df.empty:
      #raise ValueError(f"No data returned for {ticker}. Try again in 30–60 seconds.")


#def load_csv(ticker: str):
    #path = os.path.join(BASE_DIR, "data", f"{ticker}.csv")
    #print("Loading:", path)
    #df = pd.read_csv(path)
    #df = df.reset_index()
    #df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
    #df["date"] = pd.to_datetime(df["date"])

    #return df


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
   
def daily_return(df):
   df = df.copy()
   df["daily_return"] = df["close"].pct_change()
   return df

def bollinger_bands(df, window=20, num_std=2):

   df["bb_mid"] = df["close"].rolling(window).mean()
   df["bb_std"] = df["close"].rolling(window).std()
   df["bb_upper"] = df["bb_mid"] + num_std * df["bb_std"]
   df["bb_lower"] = df["bb_mid"] - num_std * df["bb_std"]

   return df

def compute_rsi(df, period=14):

   delta = df["close"].diff()

   gain = delta.clip(lower=0)
   loss = -delta.clip(upper=0)

   avg_gain = gain.rolling(period). mean()
   avg_loss = loss.rolling(period).mean()

   rs = avg_gain / avg_loss

   df["RSI"] = 100 - (100 / (1 + rs))

   return df

def compute_macd(df, fast=12, slow=26, signal=9):

   df["EMA_fast"] = df["close"].ewm(span=fast, adjust=False).mean()
   df["EMA_slow"] = df["close"].ewm(span=slow, adjust=False).mean()
   df["MACD"] = df["EMA_fast"] - df["EMA_slow"]
   df["Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()

   df["MACD_hist"] = df["MACD"] - df["Signal"]

   return df
