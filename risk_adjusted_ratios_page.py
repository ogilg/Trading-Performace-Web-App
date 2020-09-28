import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


import statistics
import yfinance as yf
import pandas as pd
import numpy as np


# DATA NECESSARY FROM DATATABLE:
#rate of return (maybe find from: number_shares * (sell_price - buy_price)...
#portfolio gains (find all positive trades and sum them up)
#portfolio losses (find all negative trades and sum up, in absolute value)

stock_codes = ['MSFT', 'TSLA', 'AAPL', 'RR.L', 'BP']
amounts = [5000, 3000, 2000, 1000, 4000]

profit_list = []
entry_dates = []
exit_dates = []
number_of_shares = []


# Finding the start and end dates
sorted_entry_dates = entry_dates.sort()
sorted_exit_dates = exit_dates.sort()
start_date = sorted_entry_dates[0]
end_date = sorted_exit_dates[-1]
print(start_date)
print(end_date)


# Finding the T-Bill rate of return between the first trade and the last trade
tbill_data = yf.Ticker('^IRX')
tbill = tbill_data.history(start=start_date, end=end_date, interval='1d', auto_adjust=False)
tbill_price = tbill['Close']
tbill_return = tbill_price[-1] - tbill_price[0]
us_t_bill = format(tbill_return, '.2f')

# Finding the standard deviation of the EXCESS returns
std_excess_return = numpy.std(rate_return - us_t_bill)

# Finding the beta of the portfolio
sum_amounts = sum(amounts)
proportions = []
beta1 = []
for amount in amounts:
    proportions.append(amount/sum_amounts)
for stock_code in stock_codes:
    info = yf.Ticker(stock_code)
    beta_specific = info.info['beta']
    beta1.append((beta_specific))
beta_portfolio = np.average(beta1, weights=proportions)

# Finding the standard deviation of the DOWNSIDE returns
std_downside_return = numpy.std(negative_profit_list)



### various ratios ###
sharpe_ratio = (rate_return - us_t_bill) / std_excess_return
sortino_ratio = (rate_return - us_t_bill) / std_downside_return
calmar_ratio = (rate_return - us_t_bill) / beta_portfolio
gain_to_pain_ratio = portfolio_gains / abs(portfolio_losses)




fig1 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = sharpe_ratio,
    mode = "gauge+number+delta",
    title = {'text': "Sharpe ratio"},
    gauge = {'axis': {'range': [None, 4]},
            'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 1], 'color': "red"},
                 {'range': [1, 2], 'color': "orange"},
                 {'range': [2,3], 'color': 'green'},
                 {'range': [3,4], 'color': 'darkgreen'}],
             }))

fig2 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = sortino_ratio,
    mode = "gauge+number+delta",
    title = {'text': "Sortino ratio"},
    gauge = {'axis': {'range': [None, 4]},
            'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 1], 'color': "red"},
                 {'range': [1, 2], 'color': "orange"},
                 {'range': [2,3], 'color': 'green'},
                 {'range': [3,4], 'color': 'darkgreen'}],
             }))

fig3 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = gain_to_pain_ratio,
    mode = "gauge+number+delta",
    title = {'text': "Gain to Pain ratio"},
    gauge = {'axis': {'range': [None, 4]},
            'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 1], 'color': "red"},
                 {'range': [1, 2], 'color': "orange"},
                 {'range': [2,3], 'color': 'green'},
                 {'range': [3,4], 'color': 'darkgreen'}],
             }))


#### Idea: use previous ratios as reference for delta

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig1),
    html.Br(),
    html.Br(),
    dcc.Graph(figure = fig2),
    html.Br(),
    html.Br(),
    dcc.Graph(figure=fig3)

])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter


### OR USE SUBPLOTS ON PLOLTY