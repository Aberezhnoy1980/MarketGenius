#!/usr/bin/env python
"""
    Custom micro library implementing interaction with Moscow Exchange ISS server
    based on MOEX docs example.

    Version: 1.0
    Developed for Python 3.x

    @copyright: 2025 by Aleksandr Berezhnoy
"""
import os
from typing import Any, Set, Dict, Tuple, Union, Type
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import logging
import pandas
from ds_app.exception.ds_exc import InvalidListLevelError
from moex_api.handlers.CSVHandle import *
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
    """
        Create url string
    """

    def __init__(self):
        self._SYSTEM_PREFIX = 'https://iss.moex.com/'
        self._NAMESPACE = {'trading_system': 'iss', 'trading_results': 'iss/history'}
        self.DEFAULT_EMB = {'engines': 'stock', 'markets': 'shares'}
        self.templates = {
            'history_by_date': 'http://iss.moex.com/iss/history/engines/{engine}/markets/{market}/boards/{board}/securities.{format}?date={date}',
            'history_by_sec': 'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{secID}.{format}?iss.only=history',
            'tickers': 'https://iss.moex.com/iss/engines/stock/markets/shares/securities.{format}',
            'MOEX_secs': 'https://iss.moex.com/iss/securities.xml?group_by=group&group_by_filter=stock_shares',
        }

    def build_url(self, response_format: str = 'json',
                  namespace: str = 'trading_system',
                  emb: Dict[str, str] = None,
                  sec_id: str = None,
                  params: Dict[str, str] = None):
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
            user: username in MOEX Passport to access real-time data and history
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
        """Make a GET request with Basic Authentication."""
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
        """Repeat auth request if failed last time or cookie expired."""
        if not self.passport or self._is_cookie_expired():
            self.auth()
        if self.passport and not self._is_cookie_expired():
            return True
        return False


class MicexISSDataHandler:
    """ Data handler which will be called
    by the ISS client to handle downloaded data.
    """

    def __init__(self, container: Type):
        """ The handler will have a container to store received data.
        """
        self.container = container()

    def process_the_data(self, market_data: Any):
        """ This handler method should be overridden to perform
        the processing of data returned by the server.
        """
        pass


class MicexISSClient:
    """ Methods for interacting with the MICEX ISS server.
    """

    def __init__(self, auth: MicexAuth, handler: Type[MicexISSDataHandler], container: Type):
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
        self.custom_handler = handler(container)
        self.handlers[self.custom_handler.__class__.__name__] = self.custom_handler
        self.url_builder = UrlBuilder()

    def get_share_listing(self) -> Set[Tuple[str, str, str, str, int]]:
        """Get list of shares and listing level

        Returns:
            set: Tuples of the unique names of the securities with listing level
        """
        url = self.url_builder.build_url(
            response_format='json',
            namespace='trading_system',
            emb=self.url_builder.DEFAULT_EMB
        )

        jres = requests.get(url).json()

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

    def get_history_csv(self, list_level: Union[int, None] = None,
                        sec_ids: Union[Set[str], None] = None,
                        filepath: Union[str, None] = None) -> bool:
        """Get historical data and convert it in csv or parquet format"""
        handler = self.handlers['csv']
        # handler.container.__setattr__('filepath', filepath)
        # handler.container.set_pathfile(filepath=filepath)

        emb = {'engines': 'stock', 'markets': 'shares'}
        params = {'iss.only': 'history'}

        if list_level and list_level not in range(1, 4):
            raise InvalidListLevelError('No shares found for the provided list level.')
        else:
            share_list = [
                el for el in self.get_share_listing() if el[4] == list_level
            ]
        if sec_ids:
            share_list = [
                el for el in self.get_share_listing() if el[0] in sec_ids
            ]
        else:
            share_list = self.get_share_listing()

        result = {}

        for sec in tqdm(share_list):
            # Get ticker
            url = self.url_builder.build_url(
                response_format='json',
                namespace='trading_results',
                emb=emb,
                params=params,
                sec_id=sec[0],
            )
            logger.debug(f'load data for {sec[0]}')
            start = 0
            cnt = 1
            # Get column names
            columns = requests.get(url + '&start=' + str(start)).text.split()[1:][0] + '\n'
            # Send column names
            handler.process_the_data(columns)
            # Send data

            while cnt > 0:
                data = requests.get(url + '&start=' + str(start)).text.split()[1:][1:]
                handler.process_the_data(data)
                cnt = len(data)
                start = start + cnt


    @staticmethod
    def _del_null(num: Union[int, float, None]) -> Union[int, float]:
        """ replace null string with zero
        """
        return 0 if num is None else num


class CSVHandler(MicexISSDataHandler):
    pass


class DFHandler(MicexISSDataHandler):
    pass


class SQLHandler(MicexISSDataHandler):
    pass


if __name__ == '__main__':
    pass
