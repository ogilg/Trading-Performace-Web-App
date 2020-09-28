# from datetime import datetime, timedelta
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objects as go
# import yfinance as yf
# from dash.dependencies import Input, Output, State
#
# exit_quality_gauge = {'axis': {'range': [-100, 100]},
#                       'bar': {'color': "black"},
#                       'steps': [
#                           {'range': [-100, 0], 'color': "red"},
#                           {'range': [0, 50], 'color': "orange"},
#                           {'range': [50, 75], 'color': 'green'},
#                           {'range': [75, 100], 'color': 'darkgreen'}],
#                       }
#
# exit_quality_fig = go.Figure()
# exit_quality_fig.add_trace(go.Indicator(
#     domain={'x': [0, 1], 'y': [0, 1]},
#     value=0,
#     mode="gauge+number+delta",
#     title={'text': "Exit quality"},
#     gauge=exit_quality_gauge))
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.Input(
#         id="input_stock",
#         type='text',
#         placeholder="STOCK CODE"
#     ),
#     html.Br(),
#     dcc.Input(
#         id="input_buy",
#         type='number',
#         placeholder="BUY PRICE"
#     ),
#     html.Br(),
#     dcc.Input(
#         id="input_sell",
#         type='number',
#         placeholder="SELL PRICE"
#     ),
#     html.Br(),
#     html.Button('Within period', id='full-period', n_clicks=0),
#     html.Br(),
#     html.Button('Within 1 day of period', id='within-one-day', n_clicks=0),
#     html.Br(),
#     html.Button('Within 1 week of period', id='within-one-week', n_clicks=0),
#     html.Br(),
#     html.Button('Within 1 month of period', id='within-one-month', n_clicks=0),
#
#     html.Br(),
#     html.Br(),
#
#     dcc.DatePickerRange(
#         id='my-date-picker-range',  # ID to be used for callback
#         max_date_allowed=datetime.today(),  # maximum date allowed on the DatePickerRange component
#         initial_visible_month=datetime.today(),  # the month initially presented when the user opens the calendar
#         start_date=(datetime.today() - timedelta(30)).date(),
#         end_date=datetime.today().date(),
#         display_format='MMM Do, YY',
#         persistence=True,
#         persisted_props=['start_date'],
#         updatemode='bothdates',
#
#     ),
#     dcc.Graph(id='exit-quality-indicator', figure=exit_quality_fig)
#
# ])
#
#
# @app.callback(
#     Output('exit-quality-indicator', 'figure'),
#     [Input('my-date-picker-range', 'start_date'),
#      Input('my-date-picker-range', 'end_date'),
#      # Input("input_stock", 'code'),
#      Input('full-period', 'n_clicks'),
#      Input('within-one-day', 'n_clicks'),
#      Input('within-one-week', 'n_clicks'),
#      Input('within-one-month', 'n_clicks')],
#     # Input('input_buy', 'buy_price'),
#     # Input('input_sell', 'sell_price')],
#
#     [State('input_stock', 'value'),
#      State('input_buy', 'value'),
#      State('input_sell', 'value')]
# )
# def update_output(start_date, end_date, full_period, within_one_day, within_one_week, within_one_month, stock_code,
#                   buy_price, sell_price):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'full-period' in changed_id:
#         pass
#     elif 'within-one-day' in changed_id:
#         start_date = start_date - timedelta(1)
#         end_date = end_date + timedelta(1)
#     elif 'within-one-week' in changed_id:
#         start_date = start_date - timedelta(7)
#         end_date = end_date + timedelta(7)
#     elif 'within-one-month' in changed_id:
#         start_date = start_date - timedelta(30)
#         end_date = end_date + timedelta(30)
#
#     ticker = stock_code or 'AAPL'
#
#     stock_data = yf.download(ticker, start=start_date, end=end_date)
#
#     sorted_stock_closes = sorted(stock_data['Close'], reverse=True)
#     max_close = round(sorted_stock_closes[0], 2)
#     min_close = round(sorted_stock_closes[-1], 2)
#
#     sell_price = sell_price or 90
#     buy_price = buy_price or 100
#
#     actual_return = ((sell_price - buy_price) / buy_price) * 100
#     max_return = ((max_close - min_close) / min_close) * 100  # maybe max_close - buy_price instead
#
#     rating = (actual_return / max_return) * 100
#
#     exit_quality_fig = go.Figure()
#     exit_quality_fig.add_trace(go.Indicator(
#         domain={'x': [0, 1], 'y': [0, 1]},
#         value=rating,
#         mode="gauge+number+delta",
#         title={'text': "Exit quality"},
#         gauge=exit_quality_gauge
#     ))
#     return exit_quality_fig
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
