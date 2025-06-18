import asyncio
from bs4 import BeautifulSoup
import requests


class TelegramParser:
    CHANNEL_URL = "https://t.me/s/marketgenius_blog"

    @staticmethod
    async def get_last_two_messages():
        """Получаем два последних НЕ рекламных сообщения"""
        try:
            print(f"Запрашиваем URL: {TelegramParser.CHANNEL_URL}")
            response = requests.get(TelegramParser.CHANNEL_URL)
            print(f"Статус ответа: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            print("HTML получен, начинаем парсинг...")

            # Для отладки: сохраним HTML в файл
            with open("telegram_page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("HTML сохранён в telegram_page.html")

            # Ищем все сообщения, исключая сервисные (рекламные)
            all_messages = soup.find_all('div', class_='tgme_widget_message')
            print(f"Всего сообщений найдено: {len(all_messages)}")

            non_ad_messages = [
                msg for msg in all_messages
                if 'tgme_widget_message_service' not in ' '.join(msg.get('class', []))
            ]
            print(f"Нерекламных сообщений: {len(non_ad_messages)}")

            # Берём два самых новых (последние в списке)
            last_two = non_ad_messages[-2:] if len(non_ad_messages) >= 2 else non_ad_messages
            print(f"Выбрано сообщений для вывода: {len(last_two)}")

            result = []
            for msg in reversed(last_two):  # Чтобы новые шли первыми
                date = msg.find('time')['datetime'] if msg.find('time') else "NO_DATE"
                content = msg.find('div', class_='tgme_widget_message_text').text if msg.find('div',
                                                                                              class_='tgme_widget_message_text') else "NO_CONTENT"
                result.append({
                    "date": date,
                    "content": content.strip()
                })
                print(f"\nНайдено сообщение от {date}:")
                print(content[:100] + "...")  # Выводим первые 100 символов

            return result

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return [{"error": str(e)}]


async def main():
    print("=== Тестирование Telegram парсера ===")
    parser = TelegramParser()
    messages = await parser.get_last_two_messages()

    print("\n=== Результат ===")
    for i, msg in enumerate(messages, 1):
        print(f"\nСообщение #{i}:")
        print(f"Дата: {msg.get('date')}")
        print("Содержание:")
        print(msg.get('content', '')[:200] + "...")  # Выводим начало сообщения


if __name__ == "__main__":
    asyncio.run(main())