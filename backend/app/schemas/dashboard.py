from pydantic import BaseModel


class OverviewKPIs(BaseModel):
    total_active_customers: int
    predicted_churn_customers: int
    predicted_churn_rate: float
    high_risk_customers: int
    critical_risk_customers: int
    revenue_at_risk: float
    average_churn_probability: float


class RiskDistributionItem(BaseModel):
    level: str
    count: int


class ChurnByCategoryItem(BaseModel):
    category: str
    churn_rate: float
    count: int
    revenue_at_risk: float


class DriverCountItem(BaseModel):
    driver: str
    count: int


class OverviewCharts(BaseModel):
    risk_distribution: list[RiskDistributionItem]
    churn_by_service: list[ChurnByCategoryItem]
    churn_by_region: list[ChurnByCategoryItem]
    top_churn_drivers: list[DriverCountItem]


class OverviewResponse(BaseModel):
    kpis: OverviewKPIs
    charts: OverviewCharts
    model_version: str | None
