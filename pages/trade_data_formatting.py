from dash_table.Format import Format, Scheme, Sign, Symbol

individual_trades_columns = [{
    'id': 'STOCK CODE',
    'name': 'STOCK CODE',
    'type': 'text'
}, {
    'id': 'BUY DATE',
    'name': 'BUY DATE (YYYY-MM-DD)',
    'type': 'datetime'
},
    {
        'id': 'BUY PRICE',
        'name': u'BUY PRICE',
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
        'id': 'SELL DATE',
        'name': 'SELL DATE (YYYY-MM-DD)',
        'type': 'datetime',
    }, {
        'id': 'SELL PRICE',
        'name': u'SELL PRICE',
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
    },
    {
        'id': 'NUMBER OF SHARES',
        'name': 'NUMBER OF SHARES',
        'type': 'numeric',
        'format': Format(
            nully='N/A',
            precision=2,
            scheme=Scheme.fixed,
        ),

    }]
