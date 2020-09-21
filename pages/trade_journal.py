import base64
import io
import time
from collections import OrderedDict

import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_table
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from pages.trade_data_formatting import individual_trades_columns

from app import app
from pages.page import Page

page = Page('Trade-Journal')
page.set_path('/pages/trade-journal')

sample_trades = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))

trades_table = dash_table.DataTable(
    id='trades-table',
    columns=individual_trades_columns,
    editable=True,
    row_deletable=True,
    style_cell={'padding': '5px', 'border': '1px solid black', 'textAlign': 'center',
                'font_family': 'Arial', 'font_size': '12px', 'backgroundColor': 'ghostwhite'},  # Style the cells
    style_header={'backgroundColor': 'darkseagreen', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'center',
                  'font_family': 'arial', 'font_size': '14px', 'border': '2px solid black'},
    page_current=0,  # page number that user is on
    page_size=20  # Max amount of rows per page,
)
trade_uploader = html.Div([
    dcc.Markdown('''
    >
    > Please input your portfolio positions:
    >
    '''),
    html.Br(),
    html.Div([trades_table, ], ),
    html.Button('Add Row', id='add-rows-button', n_clicks=0),
])

trade_upload = html.Div([
    dcc.Upload(
        id='upload-spreadsheet',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        className='uploader',
        # Allow multiple files to be uploaded
        multiple=True
    ),
])

page.layout = html.Div([
    dcc.Store(id='store-trade-data', storage_type='local'),
    trade_uploader,
    html.Br(),
    html.H4("Upload excel sheet"),
    trade_upload,
    html.Div(id='trade-data-length')
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


@app.callback(
    [Output('trades-table', 'columns'), Output('trades-table', 'data')],
    [Input('trades-table', 'data_timestamp'), Input('upload-spreadsheet', 'contents'), Input('add-rows-button', 'n_clicks'), Input('store-trade-data', 'modified_timestamp')],
    [State('trades-table', 'data'), State('trades-table', 'columns'), State('upload-spreadsheet', 'filename'), State('store-trade-data', 'data')]
)
def update_trade_table(trade_table_ts, uploaded_spreadsheets, add_row_click, stored_data_timestamp, current_trade_data,
                       current_trade_data_columns, uploaded_filenames, stored_data):
    context = dash.callback_context

    if trade_table_ts is None and stored_data_timestamp is not None and stored_data is not None:
        current_trade_data = stored_data
    else:
        current_trade_data = current_trade_data or [{c['id']: '' for c in current_trade_data_columns}]

    if not context.triggered:
        input_id = 'No clicks yet'
    else:
        input_id = context.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'add-rows-button':
        current_trade_data.append({c['id']: '' for c in current_trade_data_columns})

    elif input_id == 'upload-spreadsheet':
        if uploaded_spreadsheets is not None:
            spreadsheet_data = [parse_contents(c, n) for c, n in zip(uploaded_spreadsheets, uploaded_filenames)][0]
            current_trade_data = spreadsheet_data.to_dict('records')
            current_trade_data_columns = get_columns_from_dict(current_trade_data)

    elif input_id == 'store-trade-data':
        if stored_data_timestamp is None:
            raise PreventUpdate
        current_trade_data = stored_data or [{c['id']: '' for c in individual_trades_columns}]
        try:
            current_trade_data_columns = get_columns_from_dict(current_trade_data)
        except:
            current_trade_data_columns = individual_trades_columns

    return current_trade_data_columns, current_trade_data


def get_columns_from_dict(dicts):
    return [{'name': str(i), 'id': str(i)} for i in dicts[0]]


@app.callback(
    Output('store-trade-data', 'data'),
    [Input('trades-table', 'data_timestamp'), Input('upload-spreadsheet', 'data_timestamp'), Input('add-rows-button', 'n_clicks')],
    [State('trades-table', 'data')]
)
def update_store(timestamp, uploaded_trigger, add_row_click,  table_data):
    if timestamp is None:
        raise PreventUpdate
    return table_data

@app.callback(
    Output('trade-data-length', 'children'),
    [Input('trades-table', 'data_timestamp')],
    [State('store-trade-data', 'data')]
)
def store_data_length(ts, data):
    if ts is None:
        raise PreventUpdate
    return len(data)