from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    subscriber_id: Mapped[str] = mapped_column(String)
    account_id: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    customer_type: Mapped[str] = mapped_column(String)
    registration_date: Mapped[date] = mapped_column(Date)
    activation_date: Mapped[date] = mapped_column(Date)

    subscription: Mapped["Subscription"] = relationship(back_populates="customer", uselist=False)
    usage: Mapped["CustomerUsage"] = relationship(back_populates="customer", uselist=False)
    payment: Mapped["Payment"] = relationship(back_populates="customer", uselist=False)
    complaint: Mapped["Complaint"] = relationship(back_populates="customer", uselist=False)
    network: Mapped["NetworkExperience"] = relationship(back_populates="customer", uselist=False)
    predictions: Mapped[list["ChurnPrediction"]] = relationship(back_populates="customer")


class Subscription(Base):
    __tablename__ = "subscriptions"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    service_type: Mapped[str] = mapped_column(String)
    package_name: Mapped[str] = mapped_column(String)
    subscription_status: Mapped[str] = mapped_column(String)
    activation_date: Mapped[date] = mapped_column(Date)
    expiration_date: Mapped[date] = mapped_column(Date)
    last_renewal_date: Mapped[date] = mapped_column(Date)
    number_of_renewals: Mapped[int] = mapped_column(Integer)

    customer: Mapped["Customer"] = relationship(back_populates="subscription")


class CustomerUsage(Base):
    __tablename__ = "customer_usage"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    daily_usage_gb: Mapped[float] = mapped_column(Float)
    weekly_usage_gb: Mapped[float] = mapped_column(Float)
    monthly_usage_gb: Mapped[float] = mapped_column(Float)
    usage_last_7d_gb: Mapped[float] = mapped_column(Float)
    usage_last_30d_gb: Mapped[float] = mapped_column(Float)
    usage_last_90d_gb: Mapped[float] = mapped_column(Float)
    usage_trend: Mapped[str] = mapped_column(String)
    usage_decline_pct: Mapped[float] = mapped_column(Float)
    days_since_last_activity: Mapped[int] = mapped_column(Integer)

    customer: Mapped["Customer"] = relationship(back_populates="usage")


class Payment(Base):
    __tablename__ = "payments"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    monthly_revenue: Mapped[float] = mapped_column(Float)
    arpu: Mapped[float] = mapped_column(Float)
    recharge_value: Mapped[float] = mapped_column(Float)
    recharge_frequency: Mapped[float] = mapped_column(Float)
    failed_payments: Mapped[int] = mapped_column(Integer)
    outstanding_balance: Mapped[float] = mapped_column(Float)
    revenue_trend: Mapped[str] = mapped_column(String)

    customer: Mapped["Customer"] = relationship(back_populates="payment")


class Complaint(Base):
    __tablename__ = "complaints"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    number_of_complaints: Mapped[int] = mapped_column(Integer)
    complaint_type: Mapped[str] = mapped_column(String)
    open_complaints: Mapped[int] = mapped_column(Integer)
    average_resolution_time_hours: Mapped[float] = mapped_column(Float)
    last_complaint_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="complaint")


class NetworkExperience(Base):
    __tablename__ = "network_experience"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    network_availability_pct: Mapped[float] = mapped_column(Float)
    number_of_outages: Mapped[int] = mapped_column(Integer)
    total_downtime_hours: Mapped[float] = mapped_column(Float)
    average_downtime_hours: Mapped[float] = mapped_column(Float)
    repeated_outages: Mapped[int] = mapped_column(Integer)
    average_speed_mbps: Mapped[float] = mapped_column(Float)
    latency_ms: Mapped[float] = mapped_column(Float)
    service_area: Mapped[str] = mapped_column(String)

    customer: Mapped["Customer"] = relationship(back_populates="network")


class ChurnPrediction(Base):
    __tablename__ = "churn_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"))
    churn_probability: Mapped[float] = mapped_column(Float)
    risk_score: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String)
    top_drivers: Mapped[list] = mapped_column(JSON)
    recommended_action: Mapped[str] = mapped_column(String)
    prediction_date: Mapped[datetime] = mapped_column(DateTime)
    model_version: Mapped[str] = mapped_column(String)

    customer: Mapped["Customer"] = relationship(back_populates="predictions")


class ChurnLabel(Base):
    """Internal training label: whether the customer churned in the period
    following the synthetic data snapshot. Not exposed via the API — used
    only by the ml/ training pipeline."""

    __tablename__ = "churn_labels"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), primary_key=True)
    churn_flag: Mapped[int] = mapped_column(Integer)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="risk_analyst")
