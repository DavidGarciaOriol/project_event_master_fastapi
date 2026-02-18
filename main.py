from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from routers import recintos

app = FastAPI(title="Plataforma de Venta de Entradas")

@app.get("/")
def health_check():
    return {"status": "ok"}

# En esencia, crea la API con los modelos en la BBDD, como una migration.
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(recintos.router)
