from fastapi import APIRouter, HTTPException

from api.dependencies import AccessDep
from features_db import feature_async_session_maker
from services.auth_service import AuthService
from src.schemas.analysis import AnalysisResponse
from src.services.analysis import AnalysisService
from src.repositories.analysis import AnalysisRepository

router = APIRouter(prefix="/analysis", tags=["анализ акций"])

VALID_OFFSETS = {1, 3, 7, 30, 180, 365}


@router.get("/{ticker}/forecast/{offset_days}",
            summary="Получение данных анализа по выбранной ценной бумаге",
            description="<h3>Возвращает наборы данных для визуализации</h3>",
            response_model=AnalysisResponse)
async def analyze_stock(
        ticker: str,
        offset_days: int,
        access: AccessDep
):
    """
    Анализ акции с прогнозом

    Параметры:
    - ticker: Тикер акции (например SBER)
    - offset_days: Горизонт прогноза (1, 3, 7, 30, 180, 365 дней)
    """
    if offset_days not in VALID_OFFSETS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый горизонт прогноза. Допустимые значения: {sorted(VALID_OFFSETS)}"
        )

    if access["access_type"] == "trial":
        await AuthService.decrement_trial_attempts(access["user"].id)
        async with feature_async_session_maker() as session:
            service = AnalysisService(AnalysisRepository(session))
            result = await service.analyze_stock(ticker, offset_days)
            await session.commit()
        return result
