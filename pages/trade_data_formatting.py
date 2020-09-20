from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_core_components as dcc
import dash_html_components as html

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