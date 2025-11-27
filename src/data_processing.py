from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import pandas as pd
import numpy as np
import streamlit as st
import os

def load_stock_data(stock_symbols=['AAPL', 'MSFT', 'TSLA'], data_folder='data'):
  
  all_data = []
  
  for symbol in stock_symbols:
    filepath = os.path.join(data_folder, f'{symbol}.csv')

    try:     
       df = pd.read_csv(filepath)
       df['symbol'] = symbol

       df = df.rename(columns={
                'Close/Last': 'close',
                'close/last': 'close'
            })
   
       df.columns = [c.lower().replace(" ", "_") for c in df.columns]
       df["date"] = pd.to_datetime(df["date"])

       df = df.sort_values('date')

       all_data.append(df)
       print(f"Loaded {symbol}: {len(df)} rows")

    except FileNotFoundError:
       st.error(f"file not found{filepath}")
  
  merged_df = pd.concat(all_data, ignore_index=True)

  print(merged_df.head())
  print(merged_df.tail())
  print(merged_df.columns.tolist())

  return merged_df

def get_stock_data(df, symbol):
   return df[df['symbol'] == symbol].copy().reset_index(drop=True)

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





   
