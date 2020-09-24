import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([

    dcc.Input(
        id="input",
        type='text',
        placeholder="STOCK CODE",
),
    html.Br(),
    html.Br(),

    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        #min_date_allowed = calendar_start_date,
        max_date_allowed=dt.today(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
        start_date=(dt.today()-timedelta(30)).date(),
        end_date= dt.today().date(),
        display_format='MMM Do, YY',
        persistence=True,
        persisted_props=['start_date'],
        updatemode='bothdates',

    ),

    dcc.Graph(id='mygraph')
])


@app.callback(
    Output('mygraph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input("input", 'value')],
)
def update_output(start_date, end_date, value):

    stock_code = value

    one = yf.Ticker(value)
    first = one.info
    name = first['shortName']

    df_stock = yf.download(tickers=stock_code, start=start_date, end=end_date, auto_adjust=False)
    df_index = yf.download(tickers='^GSPC', start=start_date, end=end_date, auto_adjust=False)
    df_stock = df_stock.reset_index()
    df_index = df_index.reset_index()
    for i in ['Open', 'High', 'Close', 'Low']:
        df_stock[i] = df_stock[i].astype('float64')
    for i in ['Open', 'High', 'Close', 'Low']:
        df_index[i] = df_index[i].astype('float64')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((df_stock['Close'] - df_stock['Close'][0]) / df_stock['Close'][0]) * 100,
        name=f"{stock_code.upper()} growth"
    ))
    fig.add_trace(go.Scatter(
        x=df_index['Date'],
        y=((df_index['Close'] - df_index['Close'][0]) / df_index['Close'][0]) * 100,
        name="S&P500 growth"
    ))
    fig.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((df_stock['Close'] - df_stock['Close'][0]) / df_stock['Close'][0]) * 100 - (
                    (df_index['Close'] - df_index['Close'][0]) / df_index['Close'][0]) * 100,
        name="Comparison"
    ))
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title={
            'text': f'{name.upper()} relative comparison with the S&P500',
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
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)
