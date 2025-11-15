import pandas as pd

def load_csv(path):

   df = pd.read_csv(path)

   df.columns = [c.lower().replace(" ", "_") for c in df.columns]

   df["date"] = pd.to_datetime(df["date"])

   return df