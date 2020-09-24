import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

asset_list = ['MSFT', 'AAPL', 'TSLA', 'KO', 'RR.L', '^GSPC']
#asset_name_list = []

#for asset in asset_list:
    #asset_name = ((yf.Ticker(asset)).info)['shortName']
   #asset_name_list.append(asset_name)

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            { 'label':i,'value':i} for i in (asset_list)
        ],
        value='value',
        multi =False
    ),
    html.Div(id='output-container')
])


@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    return 'this'



if __name__ == '__main__':
    app.run_server(debug=True)