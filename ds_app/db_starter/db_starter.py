#!/usr/bin/env python
"""
    Small example of interaction with Moscow Exchange ISS server.

    Version: 1.0
    Developed for Python 3.x

    Requires iss_client.py library.
    Note that the valid username and password for the MOEX ISS account
    are required in order to perform the given request for historical data.

    @copyright: 2025 by Aleksandr Berezhnoy
"""

import sys
from moex_api.iss_client import Config
from moex_api.iss_client import MicexAuth
from moex_api.iss_client import MicexISSClient
from moex_api.iss_client import MicexISSDataHandler


class MyData:
    """ Container that will be used by the handler to store data.
    Kept separately from the handler for scalability purposes: in order
    to differentiate storage and output from the processing.
    """

    def __init__(self):
        self.history = []

    def print_listing(self):
        print("=" * 96)
        print("|%15s|%15s|%30s|%15s|%15s|" % ("SECID", "SHORTNAME", "SECNAME", "SECTYPE", "LISTLEVEL"))
        print("=" * 96)
        for sec in self.history:
            print("|%15s|%15s|%30s|%15s|%15d|" % (sec[0], sec[1], sec[2], sec[3], sec[4]))
        print("=" * 96)


class MyDataHandler(MicexISSDataHandler):
    """ This handler will be receiving pieces of data from the ISS client.
    """

    def process_the_data(self, market_data):
        """ Just as an example we add all the chunks to one list.
        In real application other options should be considered because some
        server replies may be too big to be kept in memory.
        """
        self.data.history = set(self.data.history).union(market_data)
        self.data.history = set(self.data.history)
        lev1_count = 0
        lev2_count = 0
        lev3_count = 0
        for sec in self.data.history:
            if sec[4] == 1:
                lev1_count += 1
            elif sec[4] == 2:
                lev2_count += 1
            else:
                lev3_count += 1
        print(f'Голубые фишки: {lev1_count} позиций\nАкции второго эшелона {lev2_count} позиций\n'
              f'Бумаги малой капитализации и высокого риска {lev3_count} позиций')


def main():
    # u = 'berezhnoy_aa@mail.ru'
    # p = '8Pr%M$XN*q!6e@W'
    my_config = Config(user=sys.argv[1], password=sys.argv[2], proxy_url='')
    my_auth = MicexAuth(my_config)
    if my_auth.ensure_auth():
        iss = MicexISSClient(my_auth, MyDataHandler, MyData)
        iss.get_share_listing()
        iss.handler.data.print_listing()
        print(f'{len(iss.handler.data.history)} records')
    else:
        print(my_auth.ensure_auth())
        print(sys.argv[1] + sys.argv[2])


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print("Sorry:", sys.exc_info()[0], ":", sys.exc_info()[1])
