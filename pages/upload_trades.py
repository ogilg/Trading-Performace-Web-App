import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
from app import app
from pages.page import Page
from collections import OrderedDict

page = Page('Upload-Trades')
page.set_path(('/pages/upload-trades'))

sample_trades = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))
current_data = sample_trades

sample_columns=[{
            'id': 'STOCK_CODE',
            'name': 'Stock code',
            'type': 'text'
        }, {
            'id': 'BUY_DATE',
            'name': 'Buy date (YYYY-MM-DD)',
            'type': 'datetime'
        }, {
            'id': 'BUY_PRICE',
            'name': u'Buy Price',
            'type': 'numeric',
            'format': Format(
                nully='N/A',
                precision=2,
                scheme=Scheme.fixed,
                sign=Sign.parantheses,
                symbol=Symbol.yes,
                symbol_suffix=u'£'
            ),
            'on_change': {
                'action': 'coerce',
                'failure': 'default'
            },
            'validation': {
                'default': None
            }
        }, {
            'id': 'SELL_DATE',
            'name': 'Sell date (YYYY-MM-DD)',
            'type': 'datetime',
        },{
            'id': 'SELL_PRICE',
            'name': u'Sell price',
            'type': 'numeric',
            'format': Format(
                nully='N/A',
                precision=2,
                scheme=Scheme.fixed,
                sign=Sign.parantheses,
                symbol=Symbol.yes,
                symbol_suffix=u'£'
            ),
            'on_change': {
                'action': 'coerce',
                'failure': 'default'
            },
            'validation': {
                'default': None
            }
        }],

trade_table = html.Div([
    dcc.Markdown('''
    >
    > Please input your portfolio positions:
    >
    '''),
    html.Div(
        [
        dash_table.DataTable(
            id='trades-table',
            data=sample_trades.to_dict('rows'),
            columns=sample_columns,
            editable=True,
            row_deletable=True,
            style_cell={'padding': '5px', 'border': '1px solid black', 'textAlign': 'center',
                        'font_family': 'Arial', 'font_size': '12px'},  # Style the cells
            style_header={'backgroundColor': 'red', 'fontWeight': 'bold', 'fontColor': 'white', 'textAlign': 'center',
                           'font_family': 'arial', 'font_size': '14px'},  # Style the header
            page_current=0, # page number that user is on
            page_size=20  #Max amount of rows per page,
    ),],
    ),
    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
])

trade_upload = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    ])

page.layout = html.Div([
    trade_table,
    html.Br(),
    html.H4("Upload excel sheet"),
    trade_upload
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


@app.callback([Output('trades-table', 'data'), Output('trades-table', 'columns')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_table(list_of_contents, list_of_names):
    if list_of_contents is not None:
        spreadsheet_data = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)][0]
        df = spreadsheet_data
        current_data = df
        columns = [{'name': i, 'id': i} for i in df.columns]
        return df.to_dict('records'), columns


# @app.callback(
#     Output('trades-table', 'data'),
#     [State('trades-table', 'data'),
#      State('trades-table', 'columns')])
# def add_row(rows, columns):
#     rows.append({c['id']: '' for c in columns})
#     return rows
