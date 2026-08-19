from datetime import date, datetime

from pydantic import BaseModel


class DriverOut(BaseModel):
    feature: str
    description: str
    category: str


class PredictionOut(BaseModel):
    churn_probability: float
    risk_score: int
    risk_level: str
    top_drivers: list[DriverOut]
    recommended_action: str
    prediction_date: datetime
    model_version: str

    class Config:
        from_attributes = True


class CustomerRiskRow(BaseModel):
    customer_id: str
    service_type: str
    region: str
    city: str
    arpu: float
    days_since_last_activity: int
    days_since_last_renewal: int
    usage_decline_pct: float
    number_of_complaints: int
    network_availability_pct: float
    churn_probability: float
    risk_score: int
    risk_level: str
    primary_driver: str | None


class CustomerRiskPage(BaseModel):
    items: list[CustomerRiskRow]
    total: int
    page: int
    page_size: int


class SubscriptionOut(BaseModel):
    service_type: str
    package_name: str
    subscription_status: str
    activation_date: date
    expiration_date: date
    last_renewal_date: date
    number_of_renewals: int

    class Config:
        from_attributes = True


class UsageOut(BaseModel):
    daily_usage_gb: float
    weekly_usage_gb: float
    monthly_usage_gb: float
    usage_last_7d_gb: float
    usage_last_30d_gb: float
    usage_last_90d_gb: float
    usage_trend: str
    usage_decline_pct: float
    days_since_last_activity: int

    class Config:
        from_attributes = True


class PaymentOut(BaseModel):
    monthly_revenue: float
    arpu: float
    recharge_value: float
    recharge_frequency: float
    failed_payments: int
    outstanding_balance: float
    revenue_trend: str

    class Config:
        from_attributes = True


class ComplaintOut(BaseModel):
    number_of_complaints: int
    complaint_type: str
    open_complaints: int
    average_resolution_time_hours: float
    last_complaint_date: date | None

    class Config:
        from_attributes = True


class NetworkOut(BaseModel):
    network_availability_pct: float
    number_of_outages: int
    total_downtime_hours: float
    average_downtime_hours: float
    repeated_outages: int
    average_speed_mbps: float
    latency_ms: float
    service_area: str

    class Config:
        from_attributes = True


class CustomerSummary(BaseModel):
    customer_id: str
    subscriber_id: str
    account_id: str
    city: str
    region: str
    customer_type: str
    registration_date: date
    activation_date: date

    class Config:
        from_attributes = True


class CustomerProfile(BaseModel):
    customer: CustomerSummary
    subscription: SubscriptionOut
    usage: UsageOut
    payment: PaymentOut
    complaint: ComplaintOut
    network: NetworkOut
    prediction: PredictionOut | None
