from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import yfinance as yf


class DiversificationDataProcessor:
    def __init__(self, asset_list, number_of_shares):
        self.asset_list = asset_list
        self.number_of_shares = number_of_shares
        self.create_data_series()

    def create_data_series(self):
        self.traded_amounts = []
        self.country_codes = []
        self.industries = []
        self.sectors = []
        for trade_id in range(len(self.asset_list)):
            trade_info = TradeInformation(self.asset_list[trade_id], self.number_of_shares[trade_id])

            self.country_codes.append(trade_info.get_country_code())
            self.traded_amounts.append(
                trade_info.get_latest_price() * self.number_of_shares[trade_id])

            self.industries.append(trade_info.get_stock_info('industry') or 'Other')
            self.sectors.append(trade_info.get_stock_info('sector') or 'Other')
        self.compute_total_amount_traded()

    def compute_total_amount_traded(self):
        self.total_amount_traded = sum(self.traded_amounts)

    def create_country_map_figure(self):
        self.create_country_dataframe()
        map_figure = go.Figure(data=go.Choropleth(
            locations=self.map_data['ISO code'],
            z=self.map_data['Relative investment amount'],
            colorscale='Oryel',
            autocolorscale=False,
            colorbar_title='Relative investment amount (%)'
        ))
        map_figure.update_layout(
            title_text='Asset allocation per country'
        )
        return map_figure


    def create_country_dataframe(self):
        self.country_codes_filtered = []
        relative_amounts = []
        for trade_id in range(len(self.asset_list)):
            self.append_relative_amount(relative_amounts, trade_id)

        self.map_data = self.create_map_data(relative_amounts)

    def create_map_data(self, relative_amounts):
        data = pd.DataFrame(
            {'ISO code': self.country_codes_filtered, 'Relative investment amount': relative_amounts})
        grouped_data = data.groupby('ISO code')['Relative investment amount'].sum()
        final_relative_amounts = [grouped_data[country_code] for country_code in self.country_codes_filtered]
        map_data = pd.DataFrame({'ISO code': self.country_codes_filtered, 'Relative investment amount': final_relative_amounts})
        return map_data

    def append_relative_amount(self, relative_amounts, trade_id):
        if self.country_codes[trade_id] is not None:
            self.country_codes_filtered.append(self.country_codes[trade_id])
            relative_amounts.append(round((self.traded_amounts[trade_id] / self.total_amount_traded) * 100, 2))



    def create_industry_figure(self):
        industry_data = pd.DataFrame({'Industry': self.industries, 'Investment amount': self.traded_amounts})

        industry_data_figure = px.pie(industry_data, values='Investment amount', names='Industry',
                                      color_discrete_sequence=px.colors.sequential.RdBu,
                                      title='Detailed asset allocation per industry')
        industry_data_figure.update_traces(textposition='inside', textinfo='label+percent')

        return industry_data_figure

    def create_sector_figure(self):
        sector_data = pd.DataFrame({'Sector': self.sectors, 'Investment amount': self.traded_amounts})

        sector_data_figure = px.pie(sector_data, values='Investment amount', names='Sector',
                                      color_discrete_sequence=px.colors.sequential.RdBu,
                                      title='Detailed asset allocation per industry')
        sector_data_figure.update_traces(textposition='inside', textinfo='label+percent')

        return sector_data_figure


class TradeInformation:
    def __init__(self, stock_code, number_of_shares):
        self.stock_code = stock_code
        self.number_of_shares = number_of_shares
        self.create_stock_ticker()

    def create_stock_ticker(self):
        self.stock_ticker = yf.Ticker(self.stock_code)

    def get_stock_info(self, info):
        try:
            stock_info = self.stock_ticker.info[info]
        except IndexError:
            return None
        except KeyError:
            return None
        return stock_info

    def get_country_code(self):
        country_name = self.get_stock_info('country')
        if country_name is None:
            return None
        country_code = pycountry.countries.get(name=country_name).alpha_3
        return country_code

    def get_latest_price(self):
        try:
            last_day = yf.download(tickers=self.stock_code, start=date.today() - timedelta(2), end=date.today() - timedelta(1), auto_adjust=False)
        except:
            last_day = yf.download(tickers=self.stock_code, start=date.today() - timedelta(2), end=date.today() - timedelta(1), auto_adjust=False)
        return last_day['Close'][-1]
