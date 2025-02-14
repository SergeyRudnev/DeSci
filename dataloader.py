import pandas as pd
import requests
from binance.client import Client


def download_data(crypto_id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,       
        'interval': 'daily' 
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 

        data = response.json()
        
        prices = data['prices']
        market_caps = data['market_caps']
        total_volumes = data['total_volumes']
        return prices, market_caps, total_volumes
        
    except requests.exceptions.RequestException as e:
        print(f"can't load data: {e}")
        return None


def get_data(crypto_id, days):
    data = download_data(crypto_id, days)
    if data:
        prices = pd.DataFrame(data[0], columns=['timestamp', 'price'])
        market_caps = pd.DataFrame(data[1], columns=['timestamp', 'market_cap'])
        total_volumes = pd.DataFrame(data[2], columns=['timestamp', 'total_volume'])

        df = prices.merge(market_caps).merge(total_volumes)
        df.index = pd.to_datetime(df['timestamp'], unit='ms')
        df.drop(columns=['timestamp'], inplace=True)
        return df.iloc[:-1]
        

def get_binance_historical_klines(symbol, interval, start_str, end_str):
    client = Client()
    response = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(response)
    colnames = ['openTime','openPrice','highPrice','lowPrice','closePrice','volume','closeTime','quoteAssetVolume','NumberOfTrades','TakerBaseVolume','TakerQuoteVolume','Ignore']
    df.columns = colnames
    df['closeTime'] = pd.to_datetime(df['closeTime'], unit='ms')
    df.index = df['closeTime']
    return df
