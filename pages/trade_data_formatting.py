from dash_table.Format import Format, Scheme, Sign, Symbol

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
