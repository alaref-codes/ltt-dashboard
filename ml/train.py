"""Train the churn classifier and persist a versioned model artifact.

Run: python ml/train.py
"""
import json
import os
from datetime import datetime, timezone

import joblib
import numpy as np
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

import _pathsetup  # noqa: F401

from app.core.config import settings
from features import build_features, load_raw_frame

MODEL_VERSION = "v" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def main():
    raw = load_raw_frame(include_labels=True)
    X = build_features(raw)
    y = raw["churn_flag"].astype(int).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scale_pos_weight = (y_train == 0).sum() / max(1, (y_train == 1).sum())

    model = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        scale_pos_weight=scale_pos_weight,
        eval_metric="aucpr",
        random_state=42,
    )
    model.fit(X_train, y_train)

    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= 0.5).astype(int)

    metrics = {
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "pr_auc": float(average_precision_score(y_test, proba)),
        "precision": float(precision_score(y_test, preds, zero_division=0)),
        "recall": float(recall_score(y_test, preds, zero_division=0)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "churn_rate": float(y.mean()),
        "model_version": MODEL_VERSION,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "feature_columns": list(X.columns),
    }

    os.makedirs(settings.model_dir, exist_ok=True)
    model_path = os.path.join(settings.model_dir, f"churn_model_{MODEL_VERSION}.joblib")
    latest_path = os.path.join(settings.model_dir, "churn_model_latest.joblib")
    metrics_path = os.path.join(settings.model_dir, "metrics_latest.json")

    joblib.dump({"model": model, "feature_columns": list(X.columns), "version": MODEL_VERSION}, model_path)
    joblib.dump({"model": model, "feature_columns": list(X.columns), "version": MODEL_VERSION}, latest_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
