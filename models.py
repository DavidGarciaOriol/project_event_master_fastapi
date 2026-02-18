from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Recinto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    ciudad: str
    capacidad: int

    eventos: List["Evento"] = Relationship(back_populates="recinto")

class Evento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    fecha: date
    precio: float = Field(gt=0)
    tickets_vendidos: int = Field(default=0, ge=0)

    recinto_id: int = Field(foreign_key="recinto.id")
    recinto: Optional[Recinto] = Relationship(back_populates="eventos")