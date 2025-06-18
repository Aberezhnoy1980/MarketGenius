from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict


class CandleData(BaseModel):
    """Схема одной свечи"""
    time: str  # Формат "YYYY-MM-DD"
    open: float
    high: float
    low: float
    close: float


class MoexNewsItem(BaseModel):
    """Схема новости MOEX"""
    id: int
    title: str
    date: str  # "YYYY-MM-DD HH:MM:SS"
    url: str


class TelegramMessage(BaseModel):
    """Схема сообщения из Telegram"""
    date: Optional[str] = None  # ISO format
    content: Optional[str] = None


class DashboardInitResponse(BaseModel):
    """Основная схема ответа для инициализации дашборда"""
    chart_data: List[CandleData]
    moex_news: List[MoexNewsItem]
    telegram_news: Dict[str, Optional[TelegramMessage]]
