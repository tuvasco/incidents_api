from fastapi import FastAPI
from app.core.database import engine, Base
from app.api import incidents

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Incidents API", version="1.0")

app.include_router(incidents.router)

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "Incidents API up"}
