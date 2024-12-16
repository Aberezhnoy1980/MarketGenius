import requests

import apimoex
import pandas as pd
'''
https://wlm1ke.github.io/apimoex/build/html/getting_started.html# apimoex tutorial
'''

# Пример использования реализованных запросов
# История котировок SNGSP в режиме TQBR:
def get_board_hist(ticker):
    with requests.Session() as session:
        data = apimoex.get_market_history(session, ticker, columns=None)
        df = pd.DataFrame(data)
        df.set_index('TRADEDATE', inplace=True)
        print(df.head(), '\n')
        print(df.tail(), '\n')
        df.info()
        
get_board_hist('SNGSP')
    
# Пример реализации запроса с помощью клиента
# Перечень акций, торгующихся в режиме TQBR:
request_url = ('https://iss.moex.com/iss/engines/stock/'
               'markets/shares/boards/TQBR/securities.json')
arguments = {'securities.columns': ('SECID,'
                                    'REGNUMBER,'
                                    'LOTSIZE,'
                                    'SHORTNAME')}

def get_hist_from_client(request_url, arguments):
    with requests.Session() as session:
        iss = apimoex.ISSClient(session, request_url, arguments)
        data = iss.get()
        df = pd.DataFrame(data['securities'])
        df.set_index('SECID', inplace=True)
        print(df.head(), '\n')
        print(df.tail(), '\n')
        df.info()
        
# get_hist_from_client(request_url, arguments)