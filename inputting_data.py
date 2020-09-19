import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
from collections import OrderedDict
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Data input page')

df_typing_formatting = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))

app.layout = html.Div([
    dcc.Markdown('''
>
> Please input your portfolio positions:
>
''', style={'font-family': 'arial'}),

    dash_table.DataTable(
        id='adding-rows-table',
        data=df_typing_formatting.to_dict('rows'),
        columns=[{
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
        editable=True,
        row_deletable=True,
        style_cell={'padding': '5px', 'border': '1px solid black', 'textAlign': 'center',
                    'font_family': 'Arial', 'font_size': '12px', 'backgroundColor': 'ghostwhite'},  # Style the cells
        style_header={'backgroundColor': 'darkseagreen', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'center',
                       'font_family': 'arial', 'font_size': '14px', 'border': '2px solid black'},  # Style the header
        page_current=0, # page number that user is on
        page_size=10  # Max amount of rows per page,
    ),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0, style={'font_family': 'arial', 'padding':'10px', 'backgroundColor': 'black','color':'white'}),
    dcc.Markdown('''
>
> Please click one of the buttons below to change the colour theme:
>
''', style={'font-family': 'arial'}),
    html.Button('Theme 1',id='red-theme-button', n_clicks=0, style={'font_family': 'arial', 'padding': '10px','margin': '10px'}),
    html.Button('Theme 2',id='blue-theme-button', n_clicks=0, style={'font_family': 'arial', 'padding': '10px','margin': '10px'}),
    html.Button('Theme 3',id='green-theme-button', n_clicks=0, style={'font_family': 'arial', 'padding': '10px','margin': '10px'}),
])


@app.callback(
    Output('adding-rows-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('adding-rows-table', 'data'),
     State('adding-rows-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


if __name__ == '__main__':
    app.run_server(debug=True)
