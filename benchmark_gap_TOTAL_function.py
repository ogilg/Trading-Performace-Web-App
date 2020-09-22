import plotly.express as px
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html

def get_benchmark_gap_TOTAL(stock_code):
    df_stock = yf.download(tickers=stock_code, period="10y")
    y1 = round(df_stock['Close'], 2)
    y1 = (df_stock['Close'] / df_stock['Close'][0])

    df_index = yf.download(tickers='^GSPC', period="10y")
    y2 = (df_index['Close'] / df_index['Close'][0])

    y3 = y1 - y2


    fig = px.line(df_stock, y=[y1,y2,y3], title = f'{stock_code} benchmark comparison with the S&P500')
    fig.update_xaxes(
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
    fig.update_layout(
    xaxis_rangeslider_visible=False,
    title={
        'text': f'{stock_code} benchmark comparison with the S&P500',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    yaxis_title="Price",
    font=dict(
        family="arial",
        color="black"
    ),
    legend = dict(),
    legend_title_text='Legend'
)


    app = dash.Dash()
    app.layout = html.Div([
    dcc.Graph(figure=fig),
])


    app.run_server(debug=True, use_reloader=False)

#test
stock_code = 'MSFT'
plot = get_benchmark_gap_TOTAL(stock_code)
