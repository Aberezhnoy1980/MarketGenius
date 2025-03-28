# CSV example

from src.clients.moex_api.iss_client import MicexISSClient


def main():
    # u = 'berezhnoy_aa@mail.ru'
    # p = '8Pr%M$XN*q!6e@W'
    # my_config = Config(user='berezhnoy_aa@mail.ru', password='8Pr%M$XN*q!6e@W')
    # my_auth = MicexAuth(my_config)
    # if my_auth.ensure_auth():
    #     iss = MicexISSClient(my_auth)
    #     try:
    #         iss.get_history_csv(primary_board=True,
    #                             list_level=1,
    #                             sec_ids={'sber'},
    #                             filepath='/Users/alex/Desktop/sber_primary_board.csv')
    #     except InvalidArgs as e:
    #         print(e.message)
    # else:
    #     print(my_auth.ensure_auth())
    iss = MicexISSClient()
    iss.get_history_csv(
        primary_board=True,
        list_level=1,
        sec_ids={'ydex'},
        filepath='/Users/alex/Desktop/moex_client_outputs/ydex_primary_board.csv'
    )


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print("Sorry:", sys.exc_info()[0], ":", sys.exc_info()[1])
