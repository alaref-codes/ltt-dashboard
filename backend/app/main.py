from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, customers, dashboard, model
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LTT Churn Prediction API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(customers.router)
app.include_router(model.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
