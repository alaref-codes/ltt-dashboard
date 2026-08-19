"""Batch-score every customer with the latest model and persist predictions
(probability, risk level, SHAP top drivers, recommended action) to the DB.

Run: python ml/predict.py
"""
import os
from datetime import datetime, timezone

import joblib
import numpy as np

import _pathsetup  # noqa: F401

from app.core.config import settings
from app.database.session import SessionLocal
from app.models import ChurnPrediction
from explain import compute_shap_values, top_drivers_for_customer
from features import build_features, load_raw_frame


def risk_level_for_score(score: int) -> str:
    if score >= settings.risk_threshold_critical:
        return "Critical"
    if score >= settings.risk_threshold_high:
        return "High"
    if score >= settings.risk_threshold_medium:
        return "Medium"
    return "Low"


def recommended_action_for(top_category: str | None, risk_level: str, arpu: float, high_arpu_cutoff: float) -> str:
    if risk_level in ("High", "Critical") and arpu >= high_arpu_cutoff:
        return "اتصال أولوي للاحتفاظ وتقديم عرض مخصص"
    if top_category == "network":
        return "تصعيد المشكلة الفنية للفريق التقني قبل تقديم أي عرض تجاري"
    if top_category == "usage":
        return "اقتراح باقة مناسبة أو التواصل لفهم سبب انخفاض الاستخدام"
    if top_category == "complaints":
        return "حل الشكاوى المفتوحة والتواصل الاستباقي مع العميل"
    if top_category in ("renewal", "expiry"):
        return "إرسال تذكير بالتجديد وعرض تحفيزي"
    if top_category == "payment":
        return "متابعة الرصيد المستحق وتسهيل طرق الدفع"
    return "مراقبة العميل ومتابعة دورية"


def main():
    latest_path = os.path.join(settings.model_dir, "churn_model_latest.joblib")
    bundle = joblib.load(latest_path)
    model, feature_columns, version = bundle["model"], bundle["feature_columns"], bundle["version"]

    raw = load_raw_frame(include_labels=False)
    X = build_features(raw)
    X = X.reindex(columns=feature_columns, fill_value=0)

    proba = model.predict_proba(X)[:, 1]
    shap_values = compute_shap_values(model, X)

    high_arpu_cutoff = float(np.percentile(raw["arpu"], 75))
    prediction_time = datetime.now(timezone.utc)

    predictions = []
    risk_levels = []
    for i, customer_id in enumerate(raw["customer_id"]):
        score = int(round(proba[i] * 100))
        level = risk_level_for_score(score)
        drivers = top_drivers_for_customer(shap_values[i], feature_columns, X.iloc[i])
        top_category = drivers[0]["category"] if drivers else None
        action = recommended_action_for(top_category, level, float(raw["arpu"].iloc[i]), high_arpu_cutoff)
        risk_levels.append(level)

        predictions.append(
            ChurnPrediction(
                customer_id=customer_id,
                churn_probability=float(proba[i]),
                risk_score=score,
                risk_level=level,
                top_drivers=[{k: v for k, v in d.items() if k != "impact"} for d in drivers],
                recommended_action=action,
                prediction_date=prediction_time,
                model_version=version,
            )
        )

    db = SessionLocal()
    try:
        db.query(ChurnPrediction).delete()
        db.add_all(predictions)
        db.commit()
    finally:
        db.close()

    print(f"Scored {len(predictions)} customers with model {version}.")
    print(f"Risk level distribution: "
          f"Critical={risk_levels.count('Critical')}, "
          f"High={risk_levels.count('High')}, "
          f"Medium={risk_levels.count('Medium')}, "
          f"Low={risk_levels.count('Low')}")


if __name__ == "__main__":
    main()
