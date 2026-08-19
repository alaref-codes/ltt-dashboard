# PROJECT

## Purpose

Predict which LTT (Libya Telecom & Technology) internet/data customers are
at risk of churning, explain *why* each customer is at risk, and give
commercial/risk teams a prioritized, actionable view for retention.

## Users

- Senior management (executive overview)
- Risk office
- Commercial department
- Customer service
- Marketing
- Data analysis team

## Business Problem

LTT has no systematic way to identify which customers across its internet
services (4G LTE, FWA, ADSL, VDSL, FTTH) are likely to churn, why they are
at risk, or which of them are worth prioritizing for retention based on
revenue impact.

## Stack

- Frontend: Next.js 14 (App Router) + TypeScript + Tailwind CSS + Apache
  ECharts + TanStack Table + TanStack Query
- Backend: FastAPI (Python) + SQLAlchemy + Pydantic
- Database: SQLite for this phase (file-based, zero-install). Schema is
  written to be swappable to PostgreSQL/SQL Server later via connection
  string only.
- ML: Python + Pandas/NumPy/Scikit-learn/XGBoost/SHAP, run as an offline
  pipeline (`ml/`) independent of the API and frontend.
- Auth: JWT (single authenticated-user gate for this phase; full RBAC
  deferred).

## Core Features (Phase 1)

1. Executive Overview dashboard (KPIs + churn trend/risk/service/region charts)
2. Customer Risk table (filter, sort, paginate, search, CSV export)
3. Customer 360 profile page (history + churn probability + top drivers)
4. Churn prediction API backed by a trained XGBoost model
5. Explainable AI: top-3 SHAP drivers surfaced per customer prediction

## Non-Goals (Phase 1)

1. Full RBAC / roles & permissions / AD integration / audit logging
2. Segments, Geography map, Network Impact, Retention Center workflow,
   Model Monitoring, Administration pages
3. Real LTT data integration, SQL Server, on-prem deployment, scheduled
   retraining

## Data Model

See `ml/generate_synthetic_data.py` and `backend/app/models/` for the
authoritative schema. Tables: `customers`, `subscriptions`,
`customer_usage`, `payments`, `complaints`, `network_experience`,
`churn_predictions`, `users`.

## API Endpoints

```
POST /api/auth/login
GET  /api/dashboard/overview
GET  /api/customers
GET  /api/customers/{id}
GET  /api/customers/{id}/prediction
POST /api/model/predict
```

## Security Rules

- No real customer data — synthetic data only in this phase.
- No secrets committed; JWT secret via environment variable.
- Passwords hashed (bcrypt via passlib).
- Input validated server-side (Pydantic schemas).

## UI Rules

- RTL layout, Arabic UI text with English technical terms where natural.
- Responsive (desktop-first, usable on tablet/mobile).
- Loading, empty, and error states on every data view.

## Coding Rules

- ML logic never lives in the frontend or inline in API route handlers —
  it lives in `ml/` and is invoked/read by the backend only.
- Backend uses a layered structure: api → services → repositories → models.
- Reuse the shared API client and reusable KPI/table/chart components.

## Acceptance Criteria

- `ml/train.py` produces a model with ROC-AUC > 0.7 on a held-out split.
- All 6 API endpoints return real data from SQLite (not stubs).
- Overview, Customer Risk, and Customer 360 pages render real data,
  support the interactions listed above, and build/lint cleanly.

## Deployment

Not in scope this phase — local dev only (`uvicorn` + `next dev`).

## Current Status

Phase 1 (MVP vertical slice) in progress.
