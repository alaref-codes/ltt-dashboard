from sqlalchemy.orm import Session

from app.repositories import customer_repository
from app.schemas.dashboard import (
    ChurnByCategoryItem,
    DriverCountItem,
    OverviewCharts,
    OverviewKPIs,
    OverviewResponse,
    RiskDistributionItem,
)


def get_overview(db: Session) -> OverviewResponse:
    data = customer_repository.get_overview_aggregates(db)
    total_active = data["total_active"]
    scored, avg_prob, high_count, critical_count, predicted_churn_count = data["pred_stats"]

    kpis = OverviewKPIs(
        total_active_customers=total_active,
        predicted_churn_customers=predicted_churn_count or 0,
        predicted_churn_rate=round((predicted_churn_count or 0) / total_active, 4) if total_active else 0.0,
        high_risk_customers=high_count or 0,
        critical_risk_customers=critical_count or 0,
        revenue_at_risk=round(data["revenue_at_risk"], 2),
        average_churn_probability=round(avg_prob or 0.0, 4),
    )

    risk_distribution = [RiskDistributionItem(level=level, count=count) for level, count in data["risk_distribution"]]

    churn_by_service = [
        ChurnByCategoryItem(
            category=service, churn_rate=round(rate or 0, 4), count=count, revenue_at_risk=round(revenue or 0, 2)
        )
        for service, rate, count, revenue in data["by_service"]
    ]

    churn_by_region = [
        ChurnByCategoryItem(
            category=region, churn_rate=round(rate or 0, 4), count=count, revenue_at_risk=round(revenue or 0, 2)
        )
        for region, rate, count, revenue in data["by_region"]
    ]

    top_drivers = [
        DriverCountItem(driver=label, count=count) for label, count in customer_repository.get_top_driver_counts(db)
    ]

    return OverviewResponse(
        kpis=kpis,
        charts=OverviewCharts(
            risk_distribution=risk_distribution,
            churn_by_service=churn_by_service,
            churn_by_region=churn_by_region,
            top_churn_drivers=top_drivers,
        ),
        model_version=data["latest_model_version"],
    )
