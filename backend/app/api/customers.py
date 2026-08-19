from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.repositories.customer_repository import get_prediction
from app.schemas.customer import CustomerProfile, CustomerRiskPage, PredictionOut
from app.services.customer_service import get_customer_profile, list_customer_risk

router = APIRouter(prefix="/api/customers", tags=["customers"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=CustomerRiskPage)
def list_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    region: str | None = None,
    service_type: str | None = None,
    risk_level: str | None = None,
    search: str | None = None,
    sort_by: str = "risk_score",
    sort_dir: str = "desc",
    db: Session = Depends(get_db),
):
    return list_customer_risk(db, page, page_size, region, service_type, risk_level, search, sort_by, sort_dir)


@router.get("/{customer_id}", response_model=CustomerProfile)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    profile = get_customer_profile(db, customer_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Customer not found")
    return profile


@router.get("/{customer_id}/prediction", response_model=PredictionOut)
def get_customer_prediction(customer_id: str, db: Session = Depends(get_db)):
    prediction = get_prediction(db, customer_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="No prediction available for this customer")
    return prediction
