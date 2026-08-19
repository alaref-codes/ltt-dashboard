from datetime import date

from sqlalchemy.orm import Session

from app.repositories import customer_repository

# Fixed "as of" date matching the synthetic data snapshot used by the ml/ pipeline.
SNAPSHOT_TODAY = date(2026, 8, 19)
from app.schemas.customer import (
    ComplaintOut,
    CustomerProfile,
    CustomerRiskPage,
    CustomerRiskRow,
    CustomerSummary,
    NetworkOut,
    PaymentOut,
    PredictionOut,
    SubscriptionOut,
    UsageOut,
)


def list_customer_risk(
    db: Session,
    page: int,
    page_size: int,
    region: str | None,
    service_type: str | None,
    risk_level: str | None,
    search: str | None,
    sort_by: str,
    sort_dir: str,
) -> CustomerRiskPage:
    rows, total = customer_repository.get_customer_risk_page(
        db, page, page_size, region, service_type, risk_level, search, sort_by, sort_dir
    )

    items = []
    for r in rows:
        primary_driver = None
        if r.top_drivers:
            primary_driver = r.top_drivers[0].get("description")
        items.append(
            CustomerRiskRow(
                customer_id=r.customer_id,
                service_type=r.service_type,
                region=r.region,
                city=r.city,
                arpu=r.arpu,
                days_since_last_activity=r.days_since_last_activity,
                days_since_last_renewal=(SNAPSHOT_TODAY - r.last_renewal_date).days if r.last_renewal_date else 0,
                usage_decline_pct=r.usage_decline_pct,
                number_of_complaints=r.number_of_complaints,
                network_availability_pct=r.network_availability_pct,
                churn_probability=r.churn_probability or 0.0,
                risk_score=r.risk_score or 0,
                risk_level=r.risk_level or "Unscored",
                primary_driver=primary_driver,
            )
        )

    return CustomerRiskPage(items=items, total=total, page=page, page_size=page_size)


def get_customer_profile(db: Session, customer_id: str) -> CustomerProfile | None:
    data = customer_repository.get_customer_profile(db, customer_id)
    if not data:
        return None

    prediction = None
    if data["prediction"]:
        prediction = PredictionOut.model_validate(data["prediction"])

    return CustomerProfile(
        customer=CustomerSummary.model_validate(data["customer"]),
        subscription=SubscriptionOut.model_validate(data["subscription"]),
        usage=UsageOut.model_validate(data["usage"]),
        payment=PaymentOut.model_validate(data["payment"]),
        complaint=ComplaintOut.model_validate(data["complaint"]),
        network=NetworkOut.model_validate(data["network"]),
        prediction=prediction,
    )
