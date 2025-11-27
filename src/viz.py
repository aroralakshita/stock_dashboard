import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_closing_price(df, symbol=None):

    fig = px.line(
        df,
        x="date",
        y="close",
        title= symbol if symbol else "stock closing price over time",
        labels={"date": "Date", "close": "Closing Price ($)"}
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Closing Price ($)",
        template="plotly_white"
    )
    return fig

def plot_closing_price_with_ma(df, symbol=None):

    title= symbol if symbol else "Closing price with moving averages"

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

def plot_volume_vs_return(df, symbol=None):
    
    fig = px.scatter(
        df,
        x="daily_return",
        y="volume",
        size="volume",
        hover_data="date",
        title= symbol if symbol else "Volume vs Daily return",
        labels={"daily_return": "Daily Return", "volume": "Volume"}
    )

    fig.update_layout(template="plotly_white")
    return fig

def plot_candlestick_with_bbands(df, symbol=None):

    title= symbol if symbol else "Candlestick Chart with Bollinger Bands"

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
        template="plotly_white",
        xaxis_rangeslider_visible=False
    )

    return fig

def plot_rsi(df, symbol=None):

    title=symbol if symbol else "RSI Indicator"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["RSI"],
        line=dict(width=2),
        name="RSI"
    ))

    fig.add_hline(y=70, line=dict(dash="dash", width=1))
    fig.add_hline(y=30, line=dict(dash="dash", width=1))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="RSI"
    )

    return fig

def plot_macd(df, symbol=None):

    title= symbol if symbol else "MACD Indicator"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["MACD"],
        line=dict(width=2),
        name="MACD",
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Signal"],
        line=dict(width=2),
        name="Signal",
    ))

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["MACD_hist"],
        name="Histogram"
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date"
    )

    return fig

def plot_multi_stock_comparison(df_all, symbols, column='close'):
    """
    Compare multiple stocks on the same chart
    
    Args:
        df_all: Combined DataFrame with all stocks
        symbols: List of stock symbols to compare
        column: Which column to plot (default: 'close')
    """
    fig = go.Figure()
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, symbol in enumerate(symbols):
        df_stock = df_all[df_all['symbol'] == symbol]
        
        fig.add_trace(go.Scatter(
            x=df_stock['date'],
            y=df_stock[column],
            mode='lines',
            name=symbol,
            line=dict(width=2, color=colors[i % len(colors)])
        ))
    
    fig.update_layout(
        title=f"Stock Price Comparison - {', '.join(symbols)}",
        xaxis_title="Date",
        yaxis_title=f"{column.capitalize()} Price ($)",
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig
