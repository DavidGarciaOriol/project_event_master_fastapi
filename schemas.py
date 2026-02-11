from typing import Optional
from datetime import date
from sqlmodel import SQLModel

### RECINTOS

class RecintoBase(SQLModel):
    nombre: str
    ciudad: str
    capacidad: int

class CrearRecinto(RecintoBase):
    pass

class LeerRecinto(RecintoBase):
    id: int

class ActualizacionRecinto(SQLModel):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    capacidad: Optional[int] = None


### EVENTOS

class EventoBase(SQLModel):
    nombre: str
    fecha: date
    precio: float
    recinto_id: int

class CrearEvento(EventoBase):
    pass

class LeerEvento(EventoBase):
    id: int
    tickets_vendidos: int
