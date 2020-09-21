import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


df = yf.download(tickers="AAPL", period = "5d", interval="1m")
print(df)
print(df['Adj Close'])
fig = px.line(df, y='Adj Close', title = 'Hiding non-trading hours')

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter