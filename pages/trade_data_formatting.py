from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
from collections import OrderedDict

sample_trades = pd.DataFrame(OrderedDict([
    ('STOCK_CODE', ['TSLA', 'AAPL', 'BP']),
    ('BUY_DATE', ['2020-03-13', '2019-09-13', '2015-12-18']),
    ('BUY_PRICE', [109.32, 54.69, 30.15]),
    ('SELL_DATE', ['2020-08-11', '2020-08-06', '2020-06-05']),
    ('SELL_PRICE', [274.88, 113.90, 27.71])
]))

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
