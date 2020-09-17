import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
import dash_core_components as dcc
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
from collections import OrderedDict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets )

df_typing_formatting = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))



app.layout = html.Div([

    dash_table.DataTable(
        id='adding-rows-table',
        data=df_typing_formatting.to_dict('rows'),
        columns=[{
            'id': 'STOCK_CODE',
            'name': 'Stock code',
            'type': 'text',
        }, {
            'id': 'BUY_DATE',
            'name': 'Buy date',
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
            'name': 'Sell date',
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
        style_cell={'padding': '5px', 'border': '1px solid black'},
        style_header={
            'backgroundColor': 'red',
            'fontWeight': 'bold',
            'fontColor': 'white',
            #'border': '2px solid black',
    },
    ),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),

])

@app.callback(
    Output('adding-rows-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('adding-rows-table', 'data'),
     State('adding-rows-table', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


if __name__ == '__main__':
    app.run_server(debug=True)