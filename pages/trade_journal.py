import base64
import io
from collections import OrderedDict

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Scheme, Sign, Symbol

from app import app
from pages.page import Page

page = Page('Upload-Trades')
page.set_path(('/pages/trade_journal'))

sample_trades = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))
current_data = sample_trades

individual_trades_columns = [{
    'id': 'STOCK_CODE',
    'name': 'Stock code',
    'type': 'text'
}, {
    'id': 'BUY_DATE',
    'name': 'Buy date (YYYY-MM-DD)',
    'type': 'datetime'
},
    {
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
    }, {
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
    }]

spreadsheet_formats = [
    {'label': 'Individual Trades', 'value': 'Individual Trades'},
    {'label': 'By Session', 'value': 'By Session'}
]

spreadsheet_format_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='format-dropdown',
            options=spreadsheet_formats,
            value='Individual Trades',
            className='dropdown',
        )
    ]
)
trades_table = dash_table.DataTable(
    id='trades-table',
    data=sample_trades.to_dict('rows'),
    columns=individual_trades_columns,
    editable=True,
    row_deletable=True,
    style_cell={'padding': '5px', 'border': '1px solid black', 'textAlign': 'center',
                'font_family': 'Arial', 'font_size': '12px'},  # Style the cells
    style_header={'backgroundColor': 'red', 'fontWeight': 'bold', 'fontColor': 'white',
                  'textAlign': 'center',
                  'font_family': 'arial', 'font_size': '14px'},  # Style the header
    page_current=0,  # page number that user is on
    page_size=20  # Max amount of rows per page,
)
trade_uploader = html.Div([
    dcc.Markdown('''
    >
    > Please input your portfolio positions:
    >
    '''),
    spreadsheet_format_dropdown,
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
    trade_uploader,
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


@app.callback(
    [Output('trades-table', 'columns'), Output('trades-table', 'data')],
    [Input('upload-spreadsheet', 'contents'), Input('add-rows-button', 'n_clicks'), Input('format-dropdown', 'value') ],
    [State('trades-table', 'data'), State('trades-table', 'columns'), State('upload-spreadsheet', 'filename')]
)
def update_trade_table(uploaded_spreadsheets, add_row_click, column_format, current_trade_data, current_trade_data_columns, uploaded_filenames):
    context = dash.callback_context

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
            current_trade_data_columns = [{'name': i, 'id': i} for i in spreadsheet_data.columns]

    elif input_id == 'format-dropdown':
        if column_format == 'Individual Trades':
            current_trade_data_columns = individual_trades_columns
        else:
            current_trade_data_columns = [{'name': str(i), 'id': str(i)} for i in range(5)]

    return current_trade_data_columns, current_trade_data


