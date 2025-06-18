from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stock_data(self, ticker: str) -> List[Dict]:
        """Получаем ВСЕ данные по тикеру за один запрос"""
        # Основные колонки для выборки
        columns = [
            "date", "open", "high", "low", "close",
            "target_1d", "target_3d", "target_7d",
            "target_30d", "target_180d", "target_365d",
            # Финансовые показатели
            "pe_y", "dividendsPaid_q", "netDebt_q",
            # Технические индикаторы
            "rsi", "macd",
            # Макро показатели
            "brent_close", "usd_rub", "key_rate",
        ]

        # Формируем безопасный параметризованный запрос
        query = text("""
            SELECT {columns}
            FROM securities_data_1506
            WHERE secid = :ticker
        """.format(columns=", ".join(columns))).bindparams(ticker=ticker)

        result = await self.session.execute(query)
        return result.mappings().all()
