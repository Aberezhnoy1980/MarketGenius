from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union


class OHLCData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float


class ForecastPoint(BaseModel):
    date: str
    value: float
    deviation: float
    last_close: float


class FactorGroup(BaseModel):
    financial: Dict[str, Optional[float]] = Field(default_factory=dict)
    technical: Dict[str, Optional[float]] = Field(default_factory=dict)
    macro: Dict[str, Optional[float]] = Field(default_factory=dict)


class ModelMetrics(BaseModel):
    regression: Dict[str, float] = Field(default_factory=dict)
    classification: Dict[str, float] = Field(default_factory=dict)


class AnalysisResponse(BaseModel):
    ohlc: List[OHLCData] = Field(default_factory=list)
    forecast: Optional[ForecastPoint] = None
    factors: FactorGroup = Field(default_factory=FactorGroup)
    metrics: ModelMetrics = Field(default_factory=ModelMetrics)
