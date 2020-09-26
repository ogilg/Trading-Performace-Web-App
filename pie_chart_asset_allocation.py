import plotly.express as px
import yfinance as yf
import pandas as pd

## The user inputs
tickers = ['MSFT', 'BP', 'RR.L', 'KO', 'TSLA', 'TTM']
amount = [2000, 2500, 1500, 2000 , 5000, 2500]
sector_data = []
industry_data = []

# Finding the country name of yfinance
for str in tickers:
    stock = yf.Ticker(str)
    sector_data.append(stock.info['sector'])

data = {'Sector':sector_data,'Investment amount':amount}
df = pd.DataFrame(data, columns= ['Sector','Investment amount'])


fig = px.pie(df, values='Investment amount', names='Sector', color_discrete_sequence=px.colors.sequential.RdBu, title= 'Detailed asset allocation per sector')
fig.update_traces(textposition='inside', textinfo = 'label+percent')
fig.show()