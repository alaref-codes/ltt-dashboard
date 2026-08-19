import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user

router = APIRouter(prefix="/api/model", tags=["model"], dependencies=[Depends(get_current_user)])

ML_DIR = Path(__file__).resolve().parents[3] / "ml"


@router.post("/predict")
def trigger_batch_predict():
    """Dev convenience endpoint: runs the offline ml/predict.py scoring script
    as a separate process (the backend never runs ML logic inline)."""
    result = subprocess.run(
        [sys.executable, "predict.py"],
        cwd=str(ML_DIR),
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr[-2000:])
    return {"status": "ok", "output": result.stdout.strip()}
