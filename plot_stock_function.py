import plotly.express as px
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html

def get_plot_stock(stock_code):
    df = yf.download(tickers=stock_code, period = "max")
    y=round(df['Close'],2)
    fig1 = px.area(df, y=y, title = f'{stock_code} stock price')
    fig1.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count = 5, label="5Y", step="year", stepmode = "backward"),
            dict(step="all", label="Max")
        ])
    )
)
    fig1.update_layout(
    xaxis_rangeslider_visible=False,
    title={
        'text': f'{stock_code} stock price',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    yaxis_title="Price",
    font=dict(
        family="arial",
        color="black"
    )
)


    app = dash.Dash()
    app.layout = html.Div([
    dcc.Graph(figure=fig1),
])


    app.run_server(debug=True, use_reloader=False)

#test
stock_code = 'MSFT'
stock_plot = get_plot_stock(stock_code)