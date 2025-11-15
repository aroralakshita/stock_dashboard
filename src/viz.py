import plotly.express as px
import plotly.graph_objects as go

def plot_closing_price(df):

    fig = px.line(
        df,
        x="date",
        y="close",
        title="stock closing price over time",
        labels={"date": "Date", "close": "Closing Price ($)"}
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Closing Price ($)",
        template="plotly_white"
    )
    return fig

def plot_closing_price_with_ma(df, title="Closing price with moving averages"):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["close"],
            mode="lines",
            name="Close"
        )
    )

    for c in df.columns:
        if c.startswith("ma_"):
            fig.add_trace(
                go.Scatter(
                    x=df["date"][df[c].notna()],
                    y=df[c][df[c].notna()],
                    mode="lines",
                    name=c.upper()
                )
            )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_white"
    )

    return fig

def plot_volume_vs_return(df):
    df["daily_return"] = df["close"].pct_change()

    fig = px.scatter(
        df,
        x="daily_return",
        y="volume",
        size="volume",
        hover_data="date",
        title="Volums vs Daily return",
        labels={"daily_return": "Daily Return", "volume": "Volume"}
    )

    fig.update_layout(template="plotly_white")
    return fig



