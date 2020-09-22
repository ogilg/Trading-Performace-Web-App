import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime


def get_benchmark_comparison_SP500(stock_code, start_date, end_date):
    df_stock = yf.download(tickers=stock_code, start = start_date, end = end_date, auto_adjust= False)
    df_index = yf.download(tickers='^GSPC', start = start_date, end = end_date, auto_adjust= False)
    df_stock = df_stock.reset_index()
    df_index = df_index.reset_index()
    for i in ['Open', 'High', 'Close', 'Low']:
        df_stock[i] = df_stock[i].astype('float64')
    for i in ['Open', 'High', 'Close', 'Low']:
        df_index[i] = df_index[i].astype('float64')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=df_stock['Date'],
    y=((df_stock['Close']-df_stock['Close'][0])/df_stock['Close'][0])*100,
    name=f"{stock_code} growth"
))


    fig.add_trace(go.Scatter(
    x=df_index['Date'],
    y=((df_index['Close']-df_index['Close'][0])/df_index['Close'][0])*100,
    name="S&P500 growth"
))


    fig.add_trace(go.Scatter(
    x=df_stock['Date'],
    y=((df_stock['Close']-df_stock['Close'][0])/df_stock['Close'][0])*100-((df_index['Close']-df_index['Close'][0])/df_index['Close'][0])*100,
    name="Comparison"
))


    fig.update_layout(
    xaxis_rangeslider_visible=False,
    title={
        'text': f'{stock_code} benchmark comparison with the S&P500',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    yaxis_title="Growth in %",
    font=dict(
        family="arial",
        color="black"
    ),
    legend_title_text='Legend',
)

    app = dash.Dash()
    app.layout = html.Div([
    dcc.Graph(figure=fig),
])


    app.run_server(debug=True, use_reloader=False)

##TEST

start_date = datetime(2015,9,25)
end_date = datetime(2020,8,14)
stock_code = 'AAPL'
get_benchmark_comparison_SP500(stock_code,start_date,end_date)
