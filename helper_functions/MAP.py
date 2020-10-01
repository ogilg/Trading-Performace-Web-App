#imports
import yfinance as yf
import pandas as pd
import pycountry
import plotly.graph_objects as go
import numpy as np

## The user inputs
tickers = ['MSFT', 'BP', 'KO', 'TSLA', 'OR', 'TTM']
amounts = [2000, 2500, 10000, 5000, 3000, 50000]
country_names = []
rel_amounts = []

# Finding the country name of yfinance
for ticker in tickers:
    country_names.append(yf.Ticker(ticker).info['country'])

# Transforming country name to country code
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3
codes = [countries.get(country, 'Unknown code') for country in country_names]



# Finding the ISO codes
iso = []
[iso.append(x) for x in codes if x not in iso]

# Finding the relative amounts
total1 = sum(amounts)
for amount in amounts:
    rel_amounts.append(round((amount/total1)*100,2))

# Creating the dataframe for the map
data = {'ISO code':codes,'Relative investment amount':rel_amounts,'Country': country_names}
df = pd.DataFrame(data, columns= ['ISO code','Relative investment amount', 'Country'])

# Creating the array with unique countries
final_codes = np.unique(codes)
final_rel_amounts = []
df_edit = pd.DataFrame(data, columns= ['ISO code','Relative investment amount'])

for final_code in final_codes:
    final_rel_amounts.append(df_edit.groupby('ISO code')['Relative investment amount'].sum()[final_code])

final_data = {'ISO code': final_codes, 'Relative investment amount': final_rel_amounts }
final_dataframe = pd.DataFrame(final_data, columns= ['ISO code', 'Relative investment amount'])


# Creating the map
df['text'] = 'ISO code: ' + final_dataframe['ISO code']
fig = go.Figure(data=go.Choropleth(
    locations=final_dataframe['ISO code'],
    z=final_dataframe['Relative investment amount'],
    #hovertext= df['text'],
    colorscale='Oryel',
    autocolorscale=False,
    colorbar_title="Relative investment amount (%)"
))

fig.update_layout(
    title_text='Asset allocation per country')

fig.show()

