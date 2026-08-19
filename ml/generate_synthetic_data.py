"""Generate a synthetic LTT customer base with a learnable churn signal.

Run: python ml/generate_synthetic_data.py [--n-customers 6000]
"""
import argparse
import random
from datetime import date, datetime, timedelta

import numpy as np

import _pathsetup  # noqa: F401  (adds backend/ to sys.path)

from app.database.session import Base, SessionLocal, engine
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

SERVICES = ["4G LTE", "FWA", "ADSL", "VDSL", "FTTH"]
REGIONS = {
    "Tripoli": "West",
    "Zawiya": "West",
    "Misrata": "West",
    "Khoms": "West",
    "Zliten": "West",
    "Benghazi": "East",
    "Bayda": "East",
    "Tobruk": "East",
    "Ajdabiya": "East",
    "Sabha": "South",
    "Ubari": "South",
}
CITIES = list(REGIONS.keys())
PACKAGES_BY_SERVICE = {
    "4G LTE": ["4G Basic 20GB", "4G Plus 50GB", "4G Unlimited"],
    "FWA": ["FWA Home 30GB", "FWA Home 80GB", "FWA Unlimited"],
    "ADSL": ["ADSL 4Mbps", "ADSL 8Mbps"],
    "VDSL": ["VDSL 20Mbps", "VDSL 40Mbps"],
    "FTTH": ["FTTH 50Mbps", "FTTH 100Mbps", "FTTH 200Mbps"],
}
CUSTOMER_TYPES = ["Individual", "Business"]
COMPLAINT_TYPES = ["Billing", "Network Quality", "Slow Speed", "Service Outage", "Customer Support", "None"]


def rng_choice(rng: np.random.Generator, options, p=None):
    return options[rng.choice(len(options), p=p)]


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate(n_customers: int, seed: int = 42):
    rng = np.random.default_rng(seed)
    random.seed(seed)

    customers, subscriptions, usages, payments, complaints, networks, labels = [], [], [], [], [], [], []
    churn_flags = []

    for i in range(n_customers):
        customer_id = f"LTT-{i + 1:06d}"
        city = rng_choice(rng, CITIES)
        region = REGIONS[city]
        customer_type = rng_choice(rng, CUSTOMER_TYPES, p=[0.82, 0.18])
        tenure_days = int(rng.integers(30, 2500))
        registration_date = TODAY - timedelta(days=tenure_days + int(rng.integers(0, 30)))
        activation_date = registration_date + timedelta(days=int(rng.integers(0, 15)))

        customers.append(
            Customer(
                customer_id=customer_id,
                subscriber_id=f"SUB-{i + 1:06d}",
                account_id=f"ACC-{i + 1:06d}",
                city=city,
                region=region,
                customer_type=customer_type,
                registration_date=registration_date,
                activation_date=activation_date,
            )
        )

        service_type = rng_choice(rng, SERVICES, p=[0.35, 0.15, 0.1, 0.15, 0.25])
        package_name = rng_choice(rng, PACKAGES_BY_SERVICE[service_type])
        number_of_renewals = max(0, int(tenure_days / 30 * rng.uniform(0.5, 1.0)))
        last_renewal_date = TODAY - timedelta(days=int(rng.integers(0, 60)))
        expiration_date = last_renewal_date + timedelta(days=30)

        subscriptions.append(
            Subscription(
                customer_id=customer_id,
                service_type=service_type,
                package_name=package_name,
                subscription_status="active",
                activation_date=activation_date,
                expiration_date=expiration_date,
                last_renewal_date=last_renewal_date,
                number_of_renewals=number_of_renewals,
            )
        )

        base_usage = float(rng.gamma(shape=4.0, scale=8.0))
        usage_decline_pct = float(np.clip(rng.normal(15, 25), -40, 95))
        usage_trend = "Declining" if usage_decline_pct > 10 else ("Growing" if usage_decline_pct < -10 else "Stable")
        usage_last_30d = max(0.1, base_usage * (1 - usage_decline_pct / 100))
        usage_last_7d = max(0.02, usage_last_30d / 4 * rng.uniform(0.6, 1.2))
        usage_last_90d = usage_last_30d * rng.uniform(2.6, 3.2)
        days_since_last_activity = int(np.clip(rng.exponential(scale=6) + (usage_decline_pct / 100) * 20, 0, 120))

        usages.append(
            CustomerUsage(
                customer_id=customer_id,
                daily_usage_gb=round(usage_last_7d / 7, 3),
                weekly_usage_gb=round(usage_last_7d, 2),
                monthly_usage_gb=round(base_usage, 2),
                usage_last_7d_gb=round(usage_last_7d, 2),
                usage_last_30d_gb=round(usage_last_30d, 2),
                usage_last_90d_gb=round(usage_last_90d, 2),
                usage_trend=usage_trend,
                usage_decline_pct=round(usage_decline_pct, 1),
                days_since_last_activity=days_since_last_activity,
            )
        )

        arpu = float(np.clip(rng.gamma(shape=5, scale=15), 20, 600))
        revenue_trend_pct = float(np.clip(rng.normal(5, 20), -60, 60))
        revenue_trend = "Declining" if revenue_trend_pct > 10 else ("Growing" if revenue_trend_pct < -10 else "Stable")
        failed_payments = int(rng.poisson(0.3 + max(0, revenue_trend_pct) / 40))
        recharge_frequency = float(np.clip(rng.normal(3.0 - failed_payments * 0.3, 1.0), 0.2, 6))

        payments.append(
            Payment(
                customer_id=customer_id,
                monthly_revenue=round(arpu * rng.uniform(0.9, 1.1), 2),
                arpu=round(arpu, 2),
                recharge_value=round(arpu * rng.uniform(0.8, 1.3), 2),
                recharge_frequency=round(recharge_frequency, 2),
                failed_payments=failed_payments,
                outstanding_balance=round(max(0.0, rng.normal(failed_payments * 15, 10)), 2),
                revenue_trend=revenue_trend,
            )
        )

        number_of_complaints = int(rng.poisson(max(0.05, 0.4 + usage_decline_pct / 60)))
        open_complaints = int(rng.binomial(number_of_complaints, 0.25)) if number_of_complaints else 0
        complaints.append(
            Complaint(
                customer_id=customer_id,
                number_of_complaints=number_of_complaints,
                complaint_type=rng_choice(rng, COMPLAINT_TYPES) if number_of_complaints else "None",
                open_complaints=open_complaints,
                average_resolution_time_hours=round(float(rng.uniform(2, 72)), 1) if number_of_complaints else 0.0,
                last_complaint_date=(TODAY - timedelta(days=int(rng.integers(1, 120)))) if number_of_complaints else None,
            )
        )

        network_availability = float(np.clip(rng.normal(97.5, 3.5), 70, 100))
        number_of_outages = int(rng.poisson(max(0.1, (100 - network_availability) / 8)))
        total_downtime = round(float(number_of_outages * rng.uniform(0.5, 4)), 1)
        networks.append(
            NetworkExperience(
                customer_id=customer_id,
                network_availability_pct=round(network_availability, 2),
                number_of_outages=number_of_outages,
                total_downtime_hours=total_downtime,
                average_downtime_hours=round(total_downtime / number_of_outages, 2) if number_of_outages else 0.0,
                repeated_outages=1 if number_of_outages >= 3 else 0,
                average_speed_mbps=round(float(np.clip(rng.normal(35, 15), 1, 300)), 1),
                latency_ms=round(float(np.clip(rng.normal(40, 15), 5, 200)), 1),
                service_area=city,
            )
        )

        days_since_last_renewal = (TODAY - last_renewal_date).days
        days_to_expiry = (expiration_date - TODAY).days

        risk_z = (
            0.035 * usage_decline_pct
            + 0.02 * days_since_last_activity
            + 0.5 * number_of_complaints
            + 0.9 * open_complaints
            + 0.4 * number_of_outages
            + 0.03 * total_downtime
            + 0.6 * failed_payments
            + 0.015 * max(0, 5 - days_to_expiry) * 3
            - 0.02 * network_availability
            - 0.01 * min(tenure_days, 1000) / 30
            - 0.15 * number_of_renewals
        )
        noise = rng.normal(0, 1.1)
        churn_prob_latent = sigmoid(0.9 * risk_z + noise - 2.0)
        churn_flag = int(rng.random() < churn_prob_latent)
        labels.append(ChurnLabel(customer_id=customer_id, churn_flag=churn_flag))
        churn_flags.append(churn_flag)

    return customers, subscriptions, usages, payments, complaints, networks, labels, churn_flags


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-customers", type=int, default=6000)
    args = parser.parse_args()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    customers, subscriptions, usages, payments, complaints, networks, labels, churn_flags = generate(
        args.n_customers
    )

    db = SessionLocal()
    try:
        db.add_all(customers)
        db.flush()
        db.add_all(subscriptions)
        db.add_all(usages)
        db.add_all(payments)
        db.add_all(complaints)
        db.add_all(networks)
        db.add_all(labels)
        db.commit()
    finally:
        db.close()

    churn_rate = sum(churn_flags) / len(churn_flags)
    print(f"Generated {len(customers)} customers. Synthetic churn rate: {churn_rate:.1%}")


if __name__ == "__main__":
    main()
