import pandas as pd
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

def plot_candlestick_with_bbands(df, title="Candlestick Chart with Bollinger Bands"):

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Candlestick"
    ))

    if "bb_mid" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["bb_mid"],
            line=dict(width=1),
            name="BB Mid"
        ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["bb_upper"],
        line=dict(width=1),
        name="BB Upper",
        marker_color="lightgray"
    ))
    
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["bb_lower"],
        line=dict(width=1),
        name="BB Lower",
        marker_color="lightgray",
        fill="tonexty",
        fillcolor='rgba(200,200,200,0.2)'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )

    return fig
