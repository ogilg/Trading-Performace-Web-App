import base64
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.page import Page
from pages.trade_data_formatting import individual_trades_columns

page = Page('Trade-Journal')
page.set_path('/')

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
trade_table_display = html.Div([
    dcc.Markdown('''
    >
    > ##### Input your portfolio positions and click the confirm button.
    >
    '''),
    html.Br(),
    html.Div([trades_table, ], ),
    dbc.Row([
        dbc.Col([html.Button('Add Row', id='add-rows-button', n_clicks=0, style={'margin-top': '1%'})]),
        dbc.Col([dbc.Button('Confirm Trades', color="primary", className="mr-1", style={'margin-top': '1%'},
                            id='confirm-data-button')], width={'offset': 3}),
    ],
        justify='between',
    )
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
    html.Div([dcc.Store(id='store-local-data', storage_type='session')]),
    trade_table_display,
    html.H4("Upload excel sheet"),
    trade_upload,

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
        return
    return df


@app.callback(
    [Output('trades-table', 'columns'), Output('trades-table', 'data')],
    [Input('upload-spreadsheet', 'contents'),
     Input('add-rows-button', 'n_clicks')],
    [State('trades-table', 'data'), State('upload-spreadsheet', 'filename'), State('store-local-data', 'data')]
)
def update_trade_table(uploaded_spreadsheets, add_row_click, current_trade_data,
                       uploaded_filenames, stored_data):
    context = dash.callback_context
    if not context.triggered:
        input_id = 'No clicks yet'
    else:
        input_id = context.triggered[0]['prop_id'].split('.')[0]

    if stored_data is not None:
        current_trade_data = stored_data
    else:
        current_trade_data = current_trade_data or [{c['id']: '' for c in individual_trades_columns}]

    current_trade_data_columns = get_columns_from_dicts(current_trade_data)
    if input_id == 'add-rows-button':
        current_trade_data.append({c['id']: '' for c in current_trade_data_columns})

    elif input_id == 'upload-spreadsheet':
        if uploaded_spreadsheets is not None:
            spreadsheet_data = [parse_contents(c, n) for c, n in zip(uploaded_spreadsheets, uploaded_filenames)][0]
            current_trade_data = spreadsheet_data.to_dict('records')
            current_trade_data_columns = get_columns_from_dicts(current_trade_data)

    return current_trade_data_columns, current_trade_data


def get_columns_from_dicts(dicts):
    # if len(dicts) == 0:
    #     return []
    return [{'name': str(i), 'id': str(i)} for i in dicts[0]]


@app.callback(
    Output('store-local-data', 'data'),
    [Input('trades-table', 'data')]
)
def update_store(table_data):
    if trades_table is None:
        raise PreventUpdate
    return table_data


@app.callback(
    Output('store-central-data', 'data'),
    [Input('confirm-data-button', 'n_clicks')],
    [State('store-local-data', 'data')]
)
def send_data_to_central_storage(n_clicks, local_data):
    print('Sending local data to central storage')
    if n_clicks is None:
        raise PreventUpdate
    else:
        return local_data
