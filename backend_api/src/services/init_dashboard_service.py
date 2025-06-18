import aiohttp
from typing import List, Dict
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class InitDashboardService:
    MOEX_API_URL = "https://iss.moex.com/iss"
    TELEGRAM_CHANNEL_URL = "https://t.me/s/marketgenius_blog"
    TIMEOUT = 10

    async def fetch_init_data(self) -> Dict:
        """Основной метод получения всех данных для инициализации"""
        return {
            "chart_data": await self._get_moex_index_candles(),
            "moex_news": await self._get_moex_news(),
            "telegram_news": await self._get_telegram_updates()
        }

    async def _get_moex_index_candles(
            self,
            ticker: str = "IMOEX",
            # start_date: str = "2025-01-01"
    ) -> List[Dict[str, float]]:
        """Получение свечей индекса IMOEX за последние N дней"""
        url = f"{self.MOEX_API_URL}/history/engines/stock/markets/index/securities/{ticker}.json"
        params = {
            'iss.only': 'history',
            'history.columns': 'TRADEDATE,OPEN,LOW,HIGH,CLOSE',
            'sort_order': 'desc',
            # 'from': start_date
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=self.TIMEOUT) as response:
                    data = await response.json()
                    return self._process_candle_data(data.get('history', {}).get('data', []))
        except Exception as e:
            logger.error(f"MOEX candles error: {str(e)}")
            return []

    def _process_candle_data(self, raw_data: List) -> List[Dict]:
        """Обработка сырых данных свечей с защитой от None"""
        processed = []
        for item in raw_data:
            try:
                processed.append({
                    "time": item[0],
                    "open": float(item[1]) if item[1] is not None else 0.0,
                    "low": float(item[2]) if item[2] is not None else 0.0,
                    "high": float(item[3]) if item[3] is not None else 0.0,
                    "close": float(item[4]) if item[4] is not None else 0.0
                })
            except (IndexError, TypeError, ValueError) as e:
                logger.warning(f"Failed to process candle data: {str(e)}")
        # return processed[:30]  # Гарантируем не более 30 свечей
        return processed

    async def _get_moex_news(self, limit: int = 5) -> List[Dict]:
        """Новости MOEX с улучшенной обработкой ошибок"""
        url = f"{self.MOEX_API_URL}/sitenews.json"
        params = {
            'iss.meta': 'off'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=self.TIMEOUT) as response:
                    if response.status != 200:
                        logger.error(f"MOEX news bad status: {response.status}")
                        return []

                    data = await response.json()
                    news_data = data.get('sitenews', {}).get('data', [])

                    if not news_data:
                        logger.warning("MOEX news empty data")

                    return [{
                        "id": item[0],
                        "title": item[2],
                        "date": item[4],  # modified_at
                        "url": f"https://www.moex.com/n{item[0]}?nt=113"
                    } for item in news_data]
        except Exception as e:
            logger.error(f"MOEX news error: {str(e)}")
            return []

    async def _get_telegram_updates(self) -> Dict:
        """Оптимизированный парсер Telegram (ваша рабочая версия)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        self.TELEGRAM_CHANNEL_URL,
                        timeout=self.TIMEOUT
                ) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Ваша рабочая версия парсера:
                    all_messages = soup.find_all('div', class_='tgme_widget_message')
                    non_ad_messages = [
                        msg for msg in all_messages
                        if 'tgme_widget_message_service' not in ' '.join(msg.get('class', []))
                    ]
                    last_two = non_ad_messages[-2:] if len(non_ad_messages) >= 2 else non_ad_messages

                    return {
                        "daily_summary": self._parse_telegram_msg(last_two[0]) if len(last_two) > 0 else None,
                        "sentiment_analysis": self._parse_telegram_msg(last_two[1]) if len(last_two) > 1 else None
                    }
        except Exception as e:
            logger.error(f"Telegram error: {str(e)}")
            return {"error": str(e)}

    def _parse_telegram_msg(self, msg) -> Dict:
        """Вынесенный в отдельный метод парсер сообщения"""
        return {
            "date": msg.find('time')['datetime'] if msg.find('time') else "",
            "content": msg.find('div', class_='tgme_widget_message_text').text.strip()
            if msg.find('div', class_='tgme_widget_message_text') else ""
        }
