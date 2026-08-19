"""Build the churn model feature frame from the database."""
from datetime import date

import pandas as pd
from sqlalchemy import select

import _pathsetup  # noqa: F401

from app.database.session import SessionLocal
from app.models import (
    ChurnLabel,
    Complaint,
    Customer,
    CustomerUsage,
    NetworkExperience,
    Payment,
    Subscription,
)

TODAY = date(2026, 8, 19)

CATEGORICAL_COLUMNS = ["service_type", "region", "customer_type", "usage_trend", "revenue_trend"]

NUMERIC_FEATURE_COLUMNS = [
    "customer_tenure_days",
    "days_since_last_activity",
    "days_since_last_renewal",
    "days_to_subscription_expiry",
    "number_of_renewals",
    "usage_last_30d_gb",
    "usage_decline_pct",
    "arpu",
    "recharge_frequency",
    "failed_payments",
    "outstanding_balance",
    "number_of_complaints",
    "open_complaints",
    "average_resolution_time_hours",
    "number_of_outages",
    "total_downtime_hours",
    "network_availability_pct",
    "repeated_outages",
    "average_speed_mbps",
    "latency_ms",
]


def load_raw_frame(include_labels: bool = True) -> pd.DataFrame:
    db = SessionLocal()
    try:
        rows = db.execute(
            select(
                Customer.customer_id,
                Customer.region,
                Customer.customer_type,
                Customer.registration_date,
                Subscription.service_type,
                Subscription.number_of_renewals,
                Subscription.last_renewal_date,
                Subscription.expiration_date,
                CustomerUsage.usage_last_30d_gb,
                CustomerUsage.usage_decline_pct,
                CustomerUsage.usage_trend,
                CustomerUsage.days_since_last_activity,
                Payment.arpu,
                Payment.recharge_frequency,
                Payment.failed_payments,
                Payment.outstanding_balance,
                Payment.revenue_trend,
                Complaint.number_of_complaints,
                Complaint.open_complaints,
                Complaint.average_resolution_time_hours,
                NetworkExperience.number_of_outages,
                NetworkExperience.total_downtime_hours,
                NetworkExperience.network_availability_pct,
                NetworkExperience.repeated_outages,
                NetworkExperience.average_speed_mbps,
                NetworkExperience.latency_ms,
            )
            .join(Subscription, Subscription.customer_id == Customer.customer_id)
            .join(CustomerUsage, CustomerUsage.customer_id == Customer.customer_id)
            .join(Payment, Payment.customer_id == Customer.customer_id)
            .join(Complaint, Complaint.customer_id == Customer.customer_id)
            .join(NetworkExperience, NetworkExperience.customer_id == Customer.customer_id)
        ).all()
        df = pd.DataFrame([dict(r._mapping) for r in rows])

        if include_labels:
            label_rows = db.execute(select(ChurnLabel.customer_id, ChurnLabel.churn_flag)).all()
            labels_df = pd.DataFrame([dict(r._mapping) for r in label_rows])
            df = df.merge(labels_df, on="customer_id", how="left")
    finally:
        db.close()

    today_ts = pd.Timestamp(TODAY)
    df["registration_date"] = pd.to_datetime(df["registration_date"])
    df["last_renewal_date"] = pd.to_datetime(df["last_renewal_date"])
    df["expiration_date"] = pd.to_datetime(df["expiration_date"])

    df["customer_tenure_days"] = (today_ts - df["registration_date"]).dt.days
    df["days_since_last_renewal"] = (today_ts - df["last_renewal_date"]).dt.days
    df["days_to_subscription_expiry"] = (df["expiration_date"] - today_ts).dt.days

    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_df = df[NUMERIC_FEATURE_COLUMNS + CATEGORICAL_COLUMNS].copy()
    feature_df = pd.get_dummies(feature_df, columns=CATEGORICAL_COLUMNS, dtype=int)
    feature_df.index = df["customer_id"]
    return feature_df
