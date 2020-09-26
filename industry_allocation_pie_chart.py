import plotly.express as px
import yfinance as yf
import pandas as pd

## The user inputs
tickers = ['MSFT', 'BP', 'RR.L', 'KO', 'TSLA', 'TTM','NCLH']
amount = [2000, 2500, 1500, 2000 , 5000, 2500,10000]
sector_data = []
industry_data = []

# Finding the country name of yfinance
for str in tickers:
    stock = yf.Ticker(str)
    industry_data.append(stock.info['industry'])

data = {'Industry':industry_data,'Investment amount':amount }
df = pd.DataFrame(data, columns= ['Industry','Investment amount'])


fig = px.pie(df, values='Investment amount', names='Industry', color_discrete_sequence=px.colors.sequential.RdBu, title= 'Detailed asset allocation per industry')
fig.update_traces(textposition='inside', textinfo = 'label+percent')
fig.show()