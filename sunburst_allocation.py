import plotly.express as px
import yfinance as yf
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

## The user inputs
tickers = ['MSFT', 'BP', 'RR.L', 'KO', 'TSLA', 'TTM','BA', 'NCLH']
amount = [2000, 2500, 1500, 2000 , 5000, 2500,1000, 2000]
sector_data = []
industry_data = []

# Finding the country name of yfinance
for str in tickers:
    stock = yf.Ticker(str)
    sector_data.append(stock.info['sector'])
    industry_data.append(stock.info['industry'])

# Create the dataframe for use by the chart
data = {'sector':sector_data,'amount':amount, 'industry':industry_data}
df = pd.DataFrame(data, columns= ['sector','industry','amount'])


fig = px.sunburst(df,path=['sector','industry'], values='amount', color_discrete_sequence=px.colors.sequential.RdBu, title= 'Asset allocation overview per sector and industry')
fig.update_traces(textinfo='label+percent entry')
fig.show()

## INTRODUCE A FAIL-SAFE!!! IF ONE SECTOR OR INDUSTRY IS MISSING THE WHOLE CHART FAILS. Need to simply ignore if value is inexistant
#### ALSO, lOOKS COMPLETELY DIFFERENT WHEN INTEGRATED WITH DASH