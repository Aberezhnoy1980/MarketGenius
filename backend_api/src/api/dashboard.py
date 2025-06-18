from fastapi import APIRouter, Depends

from api.dependencies import UserDep
from src.services.init_dashboard_service import InitDashboardService
from src.schemas.dashboard import DashboardInitResponse

router = APIRouter(prefix="/init", tags=["анализ акций"])


@router.get("/dashboard", response_model=DashboardInitResponse)
# @cache(expire=3600)  # Кэшируем на 1 час
async def init_dashboard(
        access: UserDep,
        service: InitDashboardService = Depends()
):
    """
    Инициализация дашборда:
    - Свечи индекса MOEX
    - Новости биржи
    - Сообщения из Telegram
    """
    return await service.fetch_init_data()
