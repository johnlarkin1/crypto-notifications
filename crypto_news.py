import gdax
import coinmarketcap
import os
import yaml
import sys
from twilio.rest import Client

file_name = 'api_keys.yaml'
numbers_to_send = ['+15136005594', '+15132407660']
twilio_number = '+15132681639'

def get_script_path():
    """Returns the filepath wrt source python execution."""
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def process_yaml_file():
    """Returns the relevant parameters from the api keys yaml file."""
    full_file_name = get_script_path() + '/' + file_name
    with open(full_file_name, 'r') as stream:
        try:
            key_dict = yaml.load(stream)
        except:
            print('There was an error with loading the yaml file. Exiting gracefully.')
            sys.exit(0)
    return key_dict

# If we want to trade algorithmically, we could use the GDAX websocket client.
def use_gdax_websocket_client(key_dict, crypto_symbol):
    auth_client = gdax.AuthenticatedClient(key_dict['gdax_key'], key_dict['gdax_api_secret'], key_dict['gdax_passphrase'])
    wsClient = gdax.WebsocketClient(url="wss://ws-feed.gdax.com", products=["BTC-USD", "ETH-USD"])

def get_crypto_market_info(crypto_symbols):
    """Returns the pertinent information concerning the cryptos specified by the parameter symbol list."""
    market = coinmarketcap.Market()
    crypto_market_info = market.ticker(limit=10)
    string_builder = '\n'
    for currency in crypto_market_info:
        if currency["symbol"] in crypto_symbols:
            string_builder += "Name: {0}\nMarketCap: ${1:,.2f} \nPrice: ${2:,.2f} \nPercentChange(7d): {3}% \nPercentChange(24hr): {4}%\n\n".format(currency['name'],
                                                                                                                                  float(currency['market_cap_usd']),
                                                                                                                                  float(currency['price_usd']),
                                                                                                                                  currency['percent_change_7d'],
                                                                                                                                  currency['percent_change_24h'])
    return string_builder

if __name__ == '__main__':
    key_dict = process_yaml_file()
    client = Client(key_dict['twilio_account_sid'], key_dict['twilio_auth_token'])
    cryptos_to_get = ['BTC', 'ETH', 'MIOTA', 'XRP']
    string_builder = get_crypto_market_info(cryptos_to_get)
    for number in numbers_to_send:
        mess = client.messages.create(
            to   = number, 
            from_= twilio_number,
            body = string_builder)
