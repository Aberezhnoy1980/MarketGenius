import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, func, Float, Date

from src.users_db import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_expiry_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    trial_attempts: Mapped[int] = mapped_column(default=3)

    date: Mapped[datetime.date] = mapped_column(Date)
    SECID: Mapped[str] = mapped_column(String)
    OPEN: Mapped[float] = mapped_column(Float)
    HIGH: Mapped[float] = mapped_column(Float)
    LOW: Mapped[float] = mapped_column(Float)
    CLOSE: Mapped[float] = mapped_column(Float)
    VOLUME: Mapped[float] = mapped_column(Float)
    WAPRICE: Mapped[float] = mapped_column(Float)
    SMA_5: Mapped[float] = mapped_column(Float)
    EMA_5: Mapped[float] = mapped_column(Float)
    SMA_10: Mapped[float] = mapped_column(Float)
    EMA_10: Mapped[float] = mapped_column(Float)
    SMA_20: Mapped[float] = mapped_column(Float)
    EMA_20: Mapped[float] = mapped_column(Float)
    SMA_50: Mapped[float] = mapped_column(Float)
    EMA_50: Mapped[float] = mapped_column(Float)
    SMA_200: Mapped[float] = mapped_column(Float)
    EMA_200: Mapped[float] = mapped_column(Float)
    RSI: Mapped[float] = mapped_column(Float)
    MACD: Mapped[float] = mapped_column(Float)
    MACD_Signal: Mapped[float] = mapped_column(Float)
    MACD_Hist: Mapped[float] = mapped_column(Float)
    BB_Middle: Mapped[float] = mapped_column(Float)
    BB_Upper: Mapped[float] = mapped_column(Float)
    BB_Lower: Mapped[float] = mapped_column(Float)
    BB_Width: Mapped[float] = mapped_column(Float)
    STOCH_K: Mapped[float] = mapped_column(Float)
    STOCH_D: Mapped[float] = mapped_column(Float)
    ATR: Mapped[float] = mapped_column(Float)
    VWAP: Mapped[float] = mapped_column(Float)
    OBV: Mapped[float] = mapped_column(Float)
    OBV_MA: Mapped[float] = mapped_column(Float)
    Williams_R: Mapped[float] = mapped_column(Float)
    Momentum: Mapped[float] = mapped_column(Float)
    Plus_DI: Mapped[float] = mapped_column(Float)
    Minus_DI: Mapped[float] = mapped_column(Float)
    ADX: Mapped[float] = mapped_column(Float)
    MFI: Mapped[float] = mapped_column(Float)
    PVO: Mapped[float] = mapped_column(Float)
    PVO_Signal: Mapped[float] = mapped_column(Float)
    PVO_Hist: Mapped[float] = mapped_column(Float)
    Chaikin_AD: Mapped[float] = mapped_column(Float)
    Chaikin_Oscillator: Mapped[float] = mapped_column(Float)
    CCI: Mapped[float] = mapped_column(Float)
    EMV: Mapped[float] = mapped_column(Float)
    A_D_Line: Mapped[float] = mapped_column(Float)
    Bull_Power: Mapped[float] = mapped_column(Float)
    Bear_Power: Mapped[float] = mapped_column(Float)
    TEMA: Mapped[float] = mapped_column(Float)
    Assets_q: Mapped[float] = mapped_column(Float)
    Assets_y: Mapped[float] = mapped_column(Float)
    CAPEX_q: Mapped[float] = mapped_column(Float)
    CAPEX_y: Mapped[float] = mapped_column(Float)
    Cash_q: Mapped[float] = mapped_column(Float)
    Cash_y: Mapped[float] = mapped_column(Float)
    Debt_q: Mapped[float] = mapped_column(Float)
    Debt_y: Mapped[float] = mapped_column(Float)
    DividendsPaid_q: Mapped[float] = mapped_column(Float)
    DividendsPaid_y: Mapped[float] = mapped_column(Float)
    EBITDA_q: Mapped[float] = mapped_column(Float)
    EBITDA_y: Mapped[float] = mapped_column(Float)
    Equity_q: Mapped[float] = mapped_column(Float)
    Equity_y: Mapped[float] = mapped_column(Float)
    NetDebt_q: Mapped[float] = mapped_column(Float)
    NetDebt_y: Mapped[float] = mapped_column(Float)
    NetProfit_q: Mapped[float] = mapped_column(Float)
    NetProfit_y: Mapped[float] = mapped_column(Float)
    OperatingCashFlow_q: Mapped[float] = mapped_column(Float)
    OperatingCashFlow_y: Mapped[float] = mapped_column(Float)
    OperatingExpenses_q: Mapped[float] = mapped_column(Float)
    OperatingExpenses_y: Mapped[float] = mapped_column(Float)
    OperatingProfit_q: Mapped[float] = mapped_column(Float)
    OperatingProfit_y: Mapped[float] = mapped_column(Float)
    Revenue_q: Mapped[float] = mapped_column(Float)
    Revenue_y: Mapped[float] = mapped_column(Float)
    BRENT_CLOSE: Mapped[float] = mapped_column(Float)
    KEY_RATE: Mapped[float] = mapped_column(Float)
    USD_RUB: Mapped[float] = mapped_column(Float)
    MRBC: Mapped[float] = mapped_column(Float)
    RTSI: Mapped[float] = mapped_column(Float)
    MCXSM: Mapped[float] = mapped_column(Float)
    IMOEX: Mapped[float] = mapped_column(Float)
    MOEXBC: Mapped[float] = mapped_column(Float)
    MOEXBMI: Mapped[float] = mapped_column(Float)
    MOEXCN: Mapped[float] = mapped_column(Float)
    MOEXIT: Mapped[float] = mapped_column(Float)
    MOEXRE: Mapped[float] = mapped_column(Float)
    MOEXEU: Mapped[float] = mapped_column(Float)
    MOEXFN: Mapped[float] = mapped_column(Float)
    MOEXINN: Mapped[float] = mapped_column(Float)
    MOEXMM: Mapped[float] = mapped_column(Float)
    MOEXOG: Mapped[float] = mapped_column(Float)
    MOEXTL: Mapped[float] = mapped_column(Float)
    MOEXTN: Mapped[float] = mapped_column(Float)
    MOEXCH: Mapped[float] = mapped_column(Float)
    ROE_y: Mapped[float] = mapped_column(Float)
    ROA_y: Mapped[float] = mapped_column(Float)
    EBITDA_Margin_y: Mapped[float] = mapped_column(Float)
    NetProfit_Margin_y: Mapped[float] = mapped_column(Float)
    Debt_Equity_q: Mapped[float] = mapped_column(Float)
    Debt_Equity_y: Mapped[float] = mapped_column(Float)
    NetDebt_EBITDA_y_q: Mapped[float] = mapped_column(Float)
    NetDebt_EBITDA_y_y: Mapped[float] = mapped_column(Float)
    EPS_y: Mapped[float] = mapped_column(Float)
    BVPS_q: Mapped[float] = mapped_column(Float)
    BVPS_y: Mapped[float] = mapped_column(Float)
    SPS_y: Mapped[float] = mapped_column(Float)
    PE_y: Mapped[float] = mapped_column(Float)
    PB_q: Mapped[float] = mapped_column(Float)
    PB_y: Mapped[float] = mapped_column(Float)
    PS_y: Mapped[float] = mapped_column(Float)
    EV_EBITDA_y: Mapped[float] = mapped_column(Float)
    target_1d: Mapped[float] = mapped_column(Float)
    target_3d: Mapped[float] = mapped_column(Float)
    target_7d: Mapped[float] = mapped_column(Float)
    target_30d: Mapped[float] = mapped_column(Float)
    target_180d: Mapped[float] = mapped_column(Float)
    AFLT_blog_score: Mapped[float] = mapped_column(Float)
    AFLT_blog_score_roll_avg_5: Mapped[float] = mapped_column(Float)
    AFLT_blog_score_roll_avg_15: Mapped[float] = mapped_column(Float)
    AFLT_blog_score_roll_avg_30: Mapped[float] = mapped_column(Float)
    WeightedIndices_blog_score: Mapped[float] = mapped_column(Float)
    WeightedIndices_blog_score_roll_avg_5: Mapped[float] = mapped_column(Float)
    WeightedIndices_blog_score_roll_avg_15: Mapped[float] = mapped_column(Float)
    WeightedIndices_blog_score_roll_avg_30: Mapped[float] = mapped_column(Float)
    AFLT_news_score: Mapped[float] = mapped_column(Float)
    AFLT_news_score_roll_avg_5: Mapped[float] = mapped_column(Float)
    AFLT_news_score_roll_avg_15: Mapped[float] = mapped_column(Float)
    AFLT_news_score_roll_avg_30: Mapped[float] = mapped_column(Float)
    WeightedIndices_news_score: Mapped[float] = mapped_column(Float)
    WeightedIndices_news_score_roll_avg_5: Mapped[float] = mapped_column(Float)
    WeightedIndices_news_score_roll_avg_15: Mapped[float] = mapped_column(Float)
    WeightedIndices_news_score_roll_avg_30: Mapped[float] = mapped_column(Float)