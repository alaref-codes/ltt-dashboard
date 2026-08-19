from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import (
    ChurnPrediction,
    Complaint,
    Customer,
    CustomerUsage,
    NetworkExperience,
    Payment,
    Subscription,
)

SORTABLE_COLUMNS = {
    "risk_score": ChurnPrediction.risk_score,
    "churn_probability": ChurnPrediction.churn_probability,
    "arpu": Payment.arpu,
    "days_since_last_activity": CustomerUsage.days_since_last_activity,
    "days_since_last_renewal": Subscription.last_renewal_date,
    "usage_decline_pct": CustomerUsage.usage_decline_pct,
    "number_of_complaints": Complaint.number_of_complaints,
}


def _base_join(query):
    return (
        query.select_from(Customer)
        .join(Subscription, Subscription.customer_id == Customer.customer_id)
        .join(CustomerUsage, CustomerUsage.customer_id == Customer.customer_id)
        .join(Payment, Payment.customer_id == Customer.customer_id)
        .join(Complaint, Complaint.customer_id == Customer.customer_id)
        .join(NetworkExperience, NetworkExperience.customer_id == Customer.customer_id)
        .outerjoin(ChurnPrediction, ChurnPrediction.customer_id == Customer.customer_id)
    )


def get_customer_risk_page(
    db: Session,
    page: int,
    page_size: int,
    region: str | None = None,
    service_type: str | None = None,
    risk_level: str | None = None,
    search: str | None = None,
    sort_by: str = "risk_score",
    sort_dir: str = "desc",
):
    stmt = _base_join(
        select(
            Customer.customer_id,
            Customer.city,
            Customer.region,
            Subscription.service_type,
            Payment.arpu,
            CustomerUsage.days_since_last_activity,
            Subscription.last_renewal_date,
            CustomerUsage.usage_decline_pct,
            Complaint.number_of_complaints,
            NetworkExperience.network_availability_pct,
            ChurnPrediction.churn_probability,
            ChurnPrediction.risk_score,
            ChurnPrediction.risk_level,
            ChurnPrediction.top_drivers,
        )
    )

    if region:
        stmt = stmt.where(Customer.region == region)
    if service_type:
        stmt = stmt.where(Subscription.service_type == service_type)
    if risk_level:
        stmt = stmt.where(ChurnPrediction.risk_level == risk_level)
    if search:
        stmt = stmt.where(Customer.customer_id.ilike(f"%{search}%"))

    count_stmt = stmt.with_only_columns(func.count()).order_by(None)
    total = db.execute(count_stmt).scalar_one()

    sort_col = SORTABLE_COLUMNS.get(sort_by, ChurnPrediction.risk_score)
    stmt = stmt.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    rows = db.execute(stmt).all()
    return rows, total


def get_customer_profile(db: Session, customer_id: str):
    customer = db.get(Customer, customer_id)
    if not customer:
        return None
    prediction = (
        db.execute(
            select(ChurnPrediction)
            .where(ChurnPrediction.customer_id == customer_id)
            .order_by(ChurnPrediction.prediction_date.desc())
        )
        .scalars()
        .first()
    )
    return {
        "customer": customer,
        "subscription": customer.subscription,
        "usage": customer.usage,
        "payment": customer.payment,
        "complaint": customer.complaint,
        "network": customer.network,
        "prediction": prediction,
    }


def get_prediction(db: Session, customer_id: str):
    return (
        db.execute(
            select(ChurnPrediction)
            .where(ChurnPrediction.customer_id == customer_id)
            .order_by(ChurnPrediction.prediction_date.desc())
        )
        .scalars()
        .first()
    )


def get_overview_aggregates(db: Session):
    total_active = db.execute(select(func.count()).select_from(Customer)).scalar_one()

    pred_stats = db.execute(
        select(
            func.count(ChurnPrediction.customer_id),
            func.avg(ChurnPrediction.churn_probability),
            func.sum(case((ChurnPrediction.risk_level == "High", 1), else_=0)),
            func.sum(case((ChurnPrediction.risk_level == "Critical", 1), else_=0)),
            func.sum(case((ChurnPrediction.churn_probability >= 0.5, 1), else_=0)),
        )
    ).one()

    revenue_at_risk = db.execute(
        _base_join(select(func.sum(Payment.arpu * ChurnPrediction.churn_probability)))
    ).scalar_one() or 0.0

    risk_distribution = db.execute(
        select(ChurnPrediction.risk_level, func.count()).group_by(ChurnPrediction.risk_level)
    ).all()

    by_service = db.execute(
        _base_join(
            select(
                Subscription.service_type,
                func.avg(ChurnPrediction.churn_probability),
                func.count(),
                func.sum(Payment.arpu * ChurnPrediction.churn_probability),
            )
        ).group_by(Subscription.service_type)
    ).all()

    by_region = db.execute(
        _base_join(
            select(
                Customer.region,
                func.avg(ChurnPrediction.churn_probability),
                func.count(),
                func.sum(Payment.arpu * ChurnPrediction.churn_probability),
            )
        ).group_by(Customer.region)
    ).all()

    latest_model_version = db.execute(
        select(ChurnPrediction.model_version).order_by(ChurnPrediction.prediction_date.desc()).limit(1)
    ).scalar_one_or_none()

    return {
        "total_active": total_active,
        "pred_stats": pred_stats,
        "revenue_at_risk": revenue_at_risk,
        "risk_distribution": risk_distribution,
        "by_service": by_service,
        "by_region": by_region,
        "latest_model_version": latest_model_version,
    }


def get_top_driver_counts(db: Session, limit: int = 8):
    predictions = db.execute(select(ChurnPrediction.top_drivers)).scalars().all()
    counts: dict[str, int] = {}
    for drivers in predictions:
        if not drivers:
            continue
        top = drivers[0]
        label = top.get("description") if isinstance(top, dict) else None
        if label:
            counts[label] = counts.get(label, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    return ranked
