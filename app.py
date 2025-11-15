from src.data_processing import clean_numeric_columns
from src.fetch_data import load_csv
from src.viz import plot_closing_price

df = load_csv("data/AAPL.csv")
df = clean_numeric_columns(df)

print(df.head())
print(df.info())

fig = plot_closing_price(df)
fig.show()