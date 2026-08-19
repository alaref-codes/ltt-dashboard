"""SHAP-based per-customer driver explanations, in Arabic, matching the
narrative style requested in the product spec (e.g. "عدم التجديد منذ 27 يوماً")."""
import numpy as np
import pandas as pd
import shap

NUMERIC_DRIVER_COLUMNS = [
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


def describe_driver(feature: str, value: float) -> tuple[str, str]:
    """Return (arabic_description, category) for a given driver feature/value."""
    if feature == "days_since_last_renewal":
        return f"عدم التجديد منذ {int(value)} يوماً", "renewal"
    if feature == "days_to_subscription_expiry":
        return f"الاشتراك على وشك الانتهاء خلال {int(value)} يوماً", "expiry"
    if feature == "usage_decline_pct":
        return f"انخفاض الاستخدام بنسبة {value:.0f}%", "usage"
    if feature == "days_since_last_activity":
        return f"عدم النشاط منذ {int(value)} يوماً", "usage"
    if feature == "number_of_complaints":
        return f"وجود {int(value)} شكاوى حديثة", "complaints"
    if feature == "open_complaints":
        return f"وجود {int(value)} شكاوى مفتوحة دون حل", "complaints"
    if feature == "average_resolution_time_hours":
        return f"بطء حل الشكاوى ({value:.0f} ساعة في المتوسط)", "complaints"
    if feature == "network_availability_pct":
        return f"انخفاض جودة الشبكة (توفر {value:.1f}%)", "network"
    if feature == "number_of_outages":
        return f"تكرار انقطاع الخدمة ({int(value)} مرات)", "network"
    if feature == "total_downtime_hours":
        return f"ساعات انقطاع مرتفعة ({value:.1f} ساعة)", "network"
    if feature == "repeated_outages":
        return "انقطاعات متكررة في الخدمة", "network"
    if feature == "latency_ms":
        return f"زمن استجابة مرتفع ({value:.0f} مللي ثانية)", "network"
    if feature == "average_speed_mbps":
        return f"سرعة إنترنت منخفضة ({value:.0f} ميجابت)", "network"
    if feature == "failed_payments":
        return f"وجود {int(value)} محاولات دفع فاشلة", "payment"
    if feature == "outstanding_balance":
        return f"رصيد مستحق غير مسدد ({value:.0f} د.ل)", "payment"
    if feature == "recharge_frequency":
        return "انخفاض تكرار الشحن/الدفع", "payment"
    if feature == "arpu":
        return "عميل ذو قيمة مرتفعة (ARPU مرتفع)", "value"
    if feature == "customer_tenure_days":
        return "عميل حديث نسبياً (قصر مدة الاشتراك)", "tenure"
    if feature == "number_of_renewals":
        return "قلة عدد مرات التجديد السابقة", "renewal"
    if feature == "usage_last_30d_gb":
        return f"انخفاض حجم الاستخدام الشهري ({value:.1f} جيجابايت)", "usage"
    return feature, "other"


def top_drivers_for_customer(
    shap_row: np.ndarray, feature_columns: list[str], feature_values: pd.Series, top_n: int = 3
) -> list[dict]:
    idx_map = [
        (i, feature_columns[i])
        for i in range(len(feature_columns))
        if feature_columns[i] in NUMERIC_DRIVER_COLUMNS
    ]
    ranked = sorted(idx_map, key=lambda pair: abs(shap_row[pair[0]]), reverse=True)[:top_n]

    drivers = []
    for i, feature in ranked:
        if shap_row[i] <= 0:
            continue
        description, category = describe_driver(feature, feature_values[feature])
        drivers.append(
            {
                "feature": feature,
                "description": description,
                "category": category,
                "impact": float(shap_row[i]),
            }
        )
    return drivers


def compute_shap_values(model, X: pd.DataFrame) -> np.ndarray:
    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(X)
    return values
