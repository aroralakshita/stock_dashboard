import plotly.express as px

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




