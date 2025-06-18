import aiomoex
import asyncio
import aiohttp


async def get_imoex_candles(interval=24, start='2025-01-01', end='2025-06-16'):
    async with aiohttp.ClientSession() as session:
        data = await aiomoex.get_market_history(
            session=session,
            security='IMOEX',
            start=start,
            end=end
        )
        print(data)


# Пример использования асинхронно
asyncio.run(get_imoex_candles())
