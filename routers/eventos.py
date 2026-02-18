from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from db import get_session
from models import Evento, Recinto
from schemas import CrearEvento, LeerEvento

router = APIRouter(prefix="/eventos", tags=["eventos"])

# Crear eventos
@router.post("/", response_model=LeerEvento)
def create_evento(evento: CrearEvento, session: Session = Depends(get_session)):
    
    if evento.precio < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo.")

    recinto = session.get(Recinto, evento.recinto_id)
    
    if not recinto:
        raise HTTPException(status_code=404, detail="El recinto no existe.")

    new_evento = Evento.model_validate(evento)
    
    session.add(new_evento)
    session.commit()
    session.refresh(new_evento)
    
    return new_evento

# Listar eventos
@router.get("/", response_model=list[LeerEvento])
def get_eventos(ciudad: str | None = Query(default=None), session: Session = Depends(get_session)):
    
    query = select(Evento)

    # Filtro por ciudad
    if ciudad:
        query = (query.join(Recinto).where(Recinto.ciudad == ciudad))

    eventos = session.exec(query).all()
    return eventos

# Compra de Tickets
@router.patch("/{evento_id}/comprar")
def comprar_tickets(evento_id: int,cantidad: int = Query(gt=0),session: Session = Depends(get_session)):
    
    evento = session.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado.")

    recinto = session.get(Recinto, evento.recinto_id)

    if evento.tickets_vendidos + cantidad > recinto.capacidad: # type: ignore
        raise HTTPException(status_code=400, detail="No hay aforo suficiente")

    evento.tickets_vendidos += cantidad
    session.add(evento)
    session.commit()

    return {
        "mensaje": "Compra realizada con éxito",
        "tickets_vendidos": evento.tickets_vendidos
    }