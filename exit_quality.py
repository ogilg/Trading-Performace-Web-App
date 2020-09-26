import yfinance as yf
from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash
import dash_html_components as html
import plotly.graph_objects as go

fig=go.Figure()
fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=0,
        mode="gauge+number+delta",
        title={'text': "Exit quality"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "black"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 75], 'color': "orange"},
                   {'range': [75, 90], 'color': 'green'},
                   {'range': [90, 100], 'color': 'darkgreen'}],
               }))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([
    dcc.Input(
        id="input_stock",
        type='text',
        placeholder="STOCK CODE"
),
    html.Br(),
    dcc.Input(
        id="input_buy",
        type='number',
        placeholder="BUY PRICE"
),
    html.Br(),
    dcc.Input(
        id="input_sell",
        type='number',
        placeholder="SELL PRICE"
),
    html.Br(),
    html.Button('Within period', id='option1', n_clicks=0),
    html.Br(),
    html.Button('Within 1 day of period', id='option2', n_clicks=0),
    html.Br(),
    html.Button('Within 1 week of period', id='option3', n_clicks=0),
    html.Br(),
    html.Button('Within 1 month of period', id='option4', n_clicks=0),

    html.Br(),
    html.Br(),

    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        max_date_allowed=datetime.today(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=datetime.today(),  # the month initially presented when the user opens the calendar
        start_date=(datetime.today()-timedelta(30)).date(),
        end_date= datetime.today().date(),
        display_format='MMM Do, YY',
        persistence=True,
        persisted_props=['start_date'],
        updatemode='bothdates',

    ),
    dcc.Graph(id='mygraph',figure=fig)

])


@app.callback(
    Output('mygraph', 'fig'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input("input_stock", 'code'),
     Input('option1', 'n_clicks'),
     Input('option2', 'n_clicks'),
     Input('option3', 'n_clicks'),
     Input('option4', 'n_clicks'),
     Input('input_buy', 'buy_price'),
     Input('input_sell', 'sell_price')],
    [State('input_stock', 'code'),
     State('input_buy', 'buy_price'),
     State('input_sell', 'sell_price')]
)
def update_output(start_date, end_date, option1, option2,option3,option4, code, buy_price, sell_price):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    ### calculations
    if option1 in changed_id:
        start = start_date
        end = end_date
    elif option2 in changed_id:
        start = start_date - timedelta(1)
        end = end_date + timedelta(1)
    elif option3 in changed_id:
        start = start_date - timedelta(7)
        end = end_date + timedelta(7)
    elif option4 in changed_id:
        start = start_date - timedelta(30)
        end = end_date + timedelta(30)

    ticker = code

    initial_data = yf.download(ticker, start=start, end=end)
    stock_price = initial_data['Close']
    max_and_min = sorted(stock_price, reverse=True)
    max_value = round(max_and_min[0], 2)
    min_value = round(max_and_min[-1], 2)

    actual_return = ((sell_price - buy_price) / buy_price) * 100
    max_return = ((max_value - min_value) / min_value) * 100

    rating = (actual_return / max_return) * 100

    fig =go.Figure()
    fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=rating,
        mode="gauge+number+delta",
        title={'text': "Exit quality"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "black"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 75], 'color': "orange"},
                   {'range': [75, 90], 'color': 'green'},
                   {'range': [90, 100], 'color': 'darkgreen'}],
               }))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)