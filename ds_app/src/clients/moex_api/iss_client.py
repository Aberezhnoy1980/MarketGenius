#!/usr/bin/env python
"""Custom micro library implementing interaction with Moscow Exchange ISS server based on MOEX docs example.

    Version: 1.0
    Developed for Python 3.x

    @copyright: 2025 by Aleksandr Berezhnoy
"""
from typing import List
import requests
from requests import Response
from requests.auth import HTTPBasicAuth
import time

import logging
from src.exception.ds_exc import InvalidArgs
from src.clients.moex_api.handlers.handle import *
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f'{__name__}.log', mode='w')
stdout_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')

file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


# TODO timeing, annotation, logging, exceptions, tests, docs


class UrlBuilder:

    def __init__(self):
        self._SYSTEM_PREFIX = 'https://iss.moex.com/'
        self._NAMESPACE = {'trading_system': 'iss', 'trading_results': 'iss/history'}
        self.DEFAULT_EMB = {'engines': 'stock', 'markets': 'shares'}

    def build_url(self, response_format: str = 'json',
                  namespace: str = 'trading_results',
                  emb: Union[Dict[str, str] | None] = None,
                  sec_id: Union[str, None] = None,
                  params: Union[Dict[str, str], None] = None):
        """A method for constructing a URL for a request to the ISS server

        Args:
            response_format (str | None, optional): Data format received from ISS server. Defaults to 'json'.
            namespace (str | None, optional): ISS-server _NAMESPACE. Defaults to 'trading_system'.
            emb (dict | None, optional): Values for engines, markets, boards. Defaults to None.
            sec_id (str | None, optional): Name of the security for filtering. Defaults to None.
            params (dict | None, optional): Url parameters. Defaults to None.

        Returns:
            str: url string
        """
        url_string = f'{self._SYSTEM_PREFIX}{self._NAMESPACE[namespace]}'
        for param, arg in emb.items():
            url_string += f'/{param}/{arg}'
        if sec_id:
            url_string += f'/securities/{sec_id}.{response_format}'
        else:
            url_string += f'/securities.{response_format}'
        if params:
            url_string += '?'
            for param, arg in params.items():
                if url_string.endswith('?'):
                    url_string += f'{param}={arg}'
                else:
                    url_string += f'&{param}={arg}'
            return url_string
        else:
            return url_string


class Config:

    def __init__(self, user: str = '', password: str = '', proxy_url: str = '', debug_level: int = 0):
        """ Container for all the configuration options:

        Args:
            user: username in MOEX Passport to access real-time data and stocks
            password: password for this user
            proxy_url: proxy URL if any is used, specified as http://proxy:port
            debug_level: 0 - no output, 1 - send debug info to stdout
        """
        self.proxy_url = proxy_url
        self.debug_level = debug_level
        self.user = user
        self.password = password
        self.auth_url = 'https://passport.moex.com/authenticate'


class MicexAuth:
    """User authentication data and functions."""

    def __init__(self, config: Config):
        self.passport = None
        self.config = config
        self.session = requests.Session()
        self.cookies = self.session.cookies
        self.cookie_name = 'MicexPassportCert'
        self.auth()

    def auth(self):
        """Makes a GET request with Basic Authentication."""
        response = self.session.get(
            self.config.auth_url,
            auth=HTTPBasicAuth(self.config.user, self.config.password)
        )
        if response.status_code == 200:
            cert = self.session.cookies.get('MicexPassportCert')
            if cert:
                self.passport = cert
                logger.info('Авторизация прошла успешно!')
            else:
                logger.warning('Ошибка: сертификат не найден в ответе.')
        else:
            logger.warning(f'Ошибка авторизации: {response.status_code}')

    def _is_cookie_expired(self) -> bool:
        for cookie in self.cookies:
            if cookie.name == self.cookie_name:
                if cookie.expires:
                    expiration_time = datetime.fromtimestamp(cookie.expires)
                    if expiration_time > datetime.now():
                        logger.info(f'Cookie "{self.cookie_name}" действителен до {expiration_time}')
                        return False
                    else:
                        logger.info(f'Cookie "{self.cookie_name}" истек {expiration_time}')
                        return True
                else:
                    logger.info(f'Cookie "{self.cookie_name}" не имеет срока действия (сессионный)')
                    return False
        logger.warning(f'Cookie "{self.cookie_name}" не найден')
        return True

    def ensure_auth(self) -> bool:
        """Repeats backend_api request if failed last time or cookie expired."""
        is_cookie_expired = self._is_cookie_expired()
        if not self.passport or is_cookie_expired:
            self.auth()
        if self.passport and not is_cookie_expired:
            return True
        return False


def timer(func):
    """

    Args:
        func:

    Returns:

    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        hours, rem = divmod(execution_time, 3600)
        minutes, seconds = divmod(rem, 60)
        milliseconds = (execution_time - int(execution_time)) * 1000

        time_str = "{:02}:{:02}:{:02}:{:03}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

        logger.info(f"Время выполнения {func.__name__}: {time_str}")
        return result

    return wrapper


def _del_null(num: Union[int, float, None]) -> Union[int, float]:
    """ Replaces null string with zero
    """
    return 0 if num is None else num


class MicexISSClient:
    """ Methods for interacting with the MICEX ISS server.
    """

    def __init__(self, auth: MicexAuth | None = None, handler: Type[MicexISSDataHandler] | None = None,
                 container: Type | None = None):
        """
        Args:
            auth: instance of the MicexAuth class with authentication info
            handler: user's handler class inherited from MicexISSDataHandler
            container: user's container class
        """
        self.auth = auth
        self.handlers = {'csv': CSVHandler(CSVContainer),
                         'sql': SQLHandler(SQLContainer),
                         'df': DFHandler(DFContainer)}
        if handler and container:
            self.custom_handler = handler(container)
            self.handlers[self.custom_handler.__class__.__name__] = self.custom_handler
        else:
            logger.info('The client will use the built-in handlers')
        self.url_builder = UrlBuilder()

    def get_stock_exchange_list(self) -> Set[Tuple[str, str, str, str, int]]:
        """Get list of shares and listing level

        Returns:
            set: Tuples of the unique names of the securities with listing level
        """
        url = self.url_builder.build_url(
            namespace='trading_system',
            emb=self.url_builder.DEFAULT_EMB
        )

        try:
            jres = self._get_get(url).json()
            jsec = jres['securities']
            jdata = jsec['data']
            jcols = jsec['columns']
            sec_idx = jcols.index('SECID')
            short_name_idx = jcols.index('SHORTNAME')
            name_idx = jcols.index('SECNAME')
            type_idx = jcols.index('SECTYPE')
            level_idx = jcols.index('LISTLEVEL')

            share_listing = set()
            for sec in jdata:
                if sec[type_idx] in ('1', '2'):
                    share_listing.add(
                        (
                            sec[sec_idx],
                            sec[short_name_idx],
                            sec[name_idx],
                            sec[type_idx],
                            sec[level_idx],
                        )
                    )
            return share_listing
        except AttributeError as e:
            logger.exception(e, exc_info=False)

    @timer
    def get_history_csv(self, emb: Dict[str, str] = None,
                        primary_board: bool = False,
                        list_level: int = None,
                        sec_ids: Set[str] = None,
                        date_interval: str = None,
                        filepath: str = None):
        """Get historical data and convert it in csv or parquet format"""
        # Define a handler
        handler = self.handlers['csv']
        # Set the file path
        handler.container.set_filepath(filepath=filepath)

        # Define params
        params = {'iss.only': 'history',
                  'history.columns': 'BOARDID,TRADEDATE,SECID,NUMTRADES,VALUE,OPEN,LOW,HIGH,LEGALCLOSEPRICE,WAPRICE,'
                                     'CLOSE,VOLUME,MARKETPRICE2,MARKETPRICE3,ADMITTEDQUOTE,MP2VALTRD,'
                                     'MARKETPRICE3TRADESVALUE,ADMITTEDVALUE,WAVAL,TRADINGSESSION,CURRENCYID,TRENDCLSPR'}
        if date_interval:
            params['from'] = date_interval.split()[0]
            params['till'] = date_interval.split()[1]
        if primary_board:
            params['marketprice_board'] = 1

        # Define a list of securities
        stocks = self._get_list_of_stocks(list_level, sec_ids)
        logger.info(f'Data will be received for the following stocks: {stocks}')
        # Write columns
        columns = list()
        columns.append(params['history.columns'].replace(',', ';'))
        handler.process_the_data(columns)

        # Getting the data
        try:
            for stock in tqdm(stocks, leave=False):
                url = self.url_builder.build_url(
                    response_format='csv',
                    emb=emb if emb else self.url_builder.DEFAULT_EMB,
                    params=params,
                    sec_id=stock
                )
                logger.info(f'Url has been built: {url}')

                # Get history cursor
                _INDEX, _PAGESIZE, _TOTAL = self._get_history_cursor(stock, url)
                start = 0
                # cnt = 1
                for _ in tqdm(range(_INDEX, _TOTAL, _PAGESIZE), leave=False):
                    data = self._get_get(url + '&start=' + str(start)).text.split()[2:]
                    handler.process_the_data(data)
                    start += len(data)
                logger.info(f'Data loading for {stock} is completed')
        except TypeError as e:
            logger.exception(e, exc_info=False)

    def transfer_data_to_db(self):
        """
        Returns:

        """
        pass

    def get_history_df(self, emb: Dict[str, str] = None,
                       primary_board: bool = False,
                       list_level: int = None,
                       sec_ids: Set[str] = None,
                       date_interval: str = None):
        """Retrieves historical data and converts it to pandas.DataFrame format
        Args:
            emb:
            primary_board:
            list_level:
            sec_ids:
            date_interval:

        Returns: pandas.DataFrame object
        """
        pass

    def get_moex_news(self):
        """Receives news from ISS and places it in the database"""
        pass

    def _get_get(self, url: str) -> Response:
        """

        Args:
            url:

        Returns:

        """
        try:
            return self.auth.session.get(url) if self.auth else requests.get(url)
        except requests.ConnectionError as e:
            logger.exception(e, exc_info=False)
        except requests.Timeout as e:
            logger.exception(e)
        except requests.RequestException as e:
            logger.exception(e)

    def _get_history_cursor(self, stock: str, url: str) -> Tuple[int, int, int]:
        _INDEX = int(self._get_get(
            url.replace('iss.only=history', 'iss.only=history.cursor&iss.meta=off')).text.split()[1].split(';')[0])
        _TOTAL = int(self._get_get(
            url.replace('iss.only=history', 'iss.only=history.cursor&iss.meta=off')).text.split()[1].split(';')[1])
        _PAGESIZE = int(self._get_get(
            url.replace('iss.only=history', 'iss.only=history.cursor&iss.meta=off')).text.split()[1].split(';')[2])
        logger.info(f'Total {_TOTAL} rows will be received for {stock}')
        logger.info(f'Data loading for {stock} has started')
        return _INDEX, _PAGESIZE, _TOTAL

    def _get_list_of_stocks(self, list_level: int | None = None, sec_ids: str | Set[str] | None = None) -> List[str]:
        try:
            if list_level or sec_ids:
                if sec_ids:
                    sec_ids = set(map(lambda el: el.upper(), sec_ids))
                    stocks = [el[0] for el in self.get_stock_exchange_list() if el[0] in sec_ids]
                    if len(stocks) == 0 and list_level:
                        if isinstance(list_level, int) and list_level in range(1, 4):
                            stocks = [el[0] for el in self.get_stock_exchange_list() if el[4] == list_level]
                        else:
                            raise InvalidArgs('Invalid both arguments: sec_ids and list_level')
                    elif len(stocks) == 0 and not list_level:
                        raise InvalidArgs('No securities found.')
                else:
                    if isinstance(list_level, int) and list_level in range(1, 4):
                        stocks = [el[0] for el in self.get_stock_exchange_list() if el[4] == list_level]
                    else:
                        raise InvalidArgs('The list level should be an integer from 1 to 3.')
            else:
                stocks = [el[0] for el in self.get_stock_exchange_list()]
            return stocks
        except TypeError as e:
            logger.exception(e, exc_info=False)


if __name__ == '__main__':
    pass
