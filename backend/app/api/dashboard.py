from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.schemas.dashboard import OverviewResponse
from app.services.dashboard_service import get_overview

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])


@router.get("/overview", response_model=OverviewResponse)
def overview(db: Session = Depends(get_db)):
    return get_overview(db)
