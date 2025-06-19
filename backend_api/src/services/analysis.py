from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from src.repositories.analysis import AnalysisRepository

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self, repo: AnalysisRepository):
        self.repo = repo

    async def analyze_stock(self, ticker: str, offset_days: int) -> Dict:
        """Основной метод анализа с новой логикой прогноза"""
        try:
            raw_data = await self.repo.get_stock_data(ticker)
            if not raw_data:
                return self._empty_response()

            sorted_data = sorted(raw_data, key=lambda x: x["date"])
            last_row = sorted_data[-1]

            return {
                "ohlc": self._prepare_ohlc(sorted_data),
                "forecast": self._prepare_forecast(last_row, offset_days),
                "factors": self._prepare_factors(last_row),
                "metrics": self._get_static_metrics()
            }
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return self._empty_response()

    def _prepare_ohlc(self, data: List[Dict]) -> List[Dict]:
        """OHLC данные с защитой от NULL"""
        return [
            {
                "date": row["date"].isoformat(),
                "open": row.get("open", 0.0) or 0.0,
                "high": row.get("high", 0.0) or 0.0,
                "low": row.get("low", 0.0) or 0.0,
                "close": row.get("close", 0.0) or 0.0
            }
            for row in data
            if row.get("date") and row.get("close") is not None
        ]

    def _prepare_forecast(self, last_row: Dict, offset_days: int) -> Optional[Dict]:
        """Новая логика прогноза с отклонениями"""
        if not last_row:
            return None

        last_close = last_row.get("close", 0.0) or 0.0
        target_col = f"target_{offset_days}d"
        deviation = last_row.get(target_col)

        forecast_value = last_close + (deviation or 0.0)

        return {
            "date": (last_row["date"] + timedelta(days=offset_days)).isoformat(),
            "value": float(forecast_value),
            "deviation": float(deviation) if deviation is not None else 0.0,
            "last_close": float(last_close)
        }

    def _prepare_factors(self, last_row: Dict) -> Dict:
        """Факторы с защитой от NULL"""
        if not last_row:
            return self._empty_factors()

        return {
            "financial": {
                "P/E": float(last_row["pe_y"]) if last_row.get("pe_y") is not None else None,
                "Dividends": float(last_row["dividendsPaid_q"]) if last_row.get(
                    "dividendsPaid_q") is not None else None,
                "Net Debt": float(last_row["netDebt_q"]) if last_row.get("netDebt_q") is not None else None
            },
            "technical": {
                "RSI": float(last_row["rsi"]) if last_row.get("rsi") is not None else None,
                "MACD": float(last_row["macd"]) if last_row.get("macd") is not None else None
            },
            "macro": {
                "Brent": float(last_row["brent_close"]) if last_row.get("brent_close") is not None else None,
                "USD/RUB": float(last_row["usd_rub"]) if last_row.get("usd_rub") is not None else None,
                "Key Rate": float(last_row["key_rate"]) if last_row.get("key_rate") is not None else None
            }
        }

    def _empty_response(self) -> Dict:
        return {
            "ohlc": [],
            "forecast": None,
            "factors": self._empty_factors(),
            "metrics": self._get_static_metrics()
        }

    def _empty_factors(self) -> Dict:
        return {
            "financial": {},
            "technical": {},
            "macro": {}
        }

    def _get_static_metrics(self) -> Dict:
        return {
            "regression": {"MAE": 0.05, "R2": 0.82},
            "classification": {"Accuracy": 0.78, "AUC": 0.85}
        }
