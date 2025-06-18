import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class TelegramParser:
    CHANNEL_URL = "https://t.me/s/marketgenius_blog"
    TIMEOUT = 10

    @staticmethod
    async def get_last_two_messages() -> List[Dict[str, str]]:
        """Получаем два последних НЕ рекламных сообщения"""
        try:
            logger.info(f"Запрос к Telegram каналу: {TelegramParser.CHANNEL_URL}")
            response = requests.get(TelegramParser.CHANNEL_URL, timeout=TelegramParser.TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            all_messages = soup.find_all('div', class_='tgme_widget_message')

            non_ad_messages = [
                msg for msg in all_messages
                if 'tgme_widget_message_service' not in ' '.join(msg.get('class', []))
            ]

            last_two = non_ad_messages[-2:] if len(non_ad_messages) >= 2 else non_ad_messages

            return [{
                "date": msg.find('time')['datetime'] if msg.find('time') else "",
                "content": msg.find('div', class_='tgme_widget_message_text').text.strip()
                if msg.find('div', class_='tgme_widget_message_text') else ""
            } for msg in reversed(last_two)]

        except Exception as e:
            logger.error(f"Ошибка парсинга Telegram: {str(e)}")
            return [{"error": f"Ошибка получения сообщений: {str(e)}"}]
