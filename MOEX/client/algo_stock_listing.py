import pandas as pd
from moexalgo import Market

stocks = Market("stocks")
all_stocks = pd.DataFrame(stocks.tickers())
print(all_stocks.columns.tolist())
listlevels = sorted(all_stocks["listlevel"].unique())
with open("stock_listing.txt", "w", encoding="utf-8") as file:
    print(f"Всего в Алгопаке доступны данные по {all_stocks.shape[0]} акциям Мосбиржи")
    print(
        f"Всего в Алгопаке доступны данные по {all_stocks.shape[0]} акциям Мосбиржи",
        file=file,
    )
    for level in listlevels:
        stocks_level = all_stocks[all_stocks["listlevel"] == level]
        print(f"Для {level} уровня листинга отобрано {stocks_level.shape[0]} акций:")
        print(
            f"Для {level} уровня листинга отобрано {stocks_level.shape[0]} акций:",
            file=file,
        )
        list_tickers = stocks_level["ticker"].tolist()
        list_shortnames = stocks_level["shortname"].tolist()
        for ticker, shortname in zip(list_tickers, list_shortnames):
            print(f"{ticker} - {shortname}")
            print(f"{ticker} - {shortname}", file=file)
        print("_" * 70)
        print("_" * 70, file=file)