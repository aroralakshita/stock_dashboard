from src.data_processing import clean_numeric_columns, moving_avg
from src.fetch_data import load_csv
from src.viz import plot_closing_price_with_ma

df = load_csv("data/AAPL.csv")
df = clean_numeric_columns(df)

print(df.head())
print(df.info())


df = moving_avg(df, windows=[20, 50])

print(df.columns)

fig = plot_closing_price_with_ma(df)
fig.show()


