from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import Recinto
from app.schemas import CrearRecinto, LeerRecinto, ActualizacionRecinto

router = APIRouter(prefix="/recintos", tags=["Recintos"])

# Crear Recinto
@router.post("/", response_model=LeerRecinto)
def create_recinto(recinto: CrearRecinto, session: Session = Depends(get_session)):
    
    new_recinto = Recinto.model_validate(recinto)
    session.add(new_recinto)
    session.commit()
    session.refresh(new_recinto)
    return new_recinto

# Listar Recintos
@router.get("/", response_model=list[LeerRecinto])
def get_recintos(session: Session = Depends(get_session)):
    
    recintos = session.exec(select(Recinto)).all()
    return recintos

# Obtener Recinto
@router.get("/{id_recinto}", response_model=LeerRecinto)
def get_recinto(id_recinto: int, session: Session = Depends(get_session)):
    
    recinto = session.get(Recinto, id_recinto)
    
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado.")
    
    return recinto

# Actualizar Recinto
@router.put("/{id_recinto}", response_model=LeerRecinto)
def update_recinto(id_recinto: int, recinto_data: ActualizacionRecinto, session: Session = Depends(get_session)):
    
    recinto = session.get(Recinto, id_recinto
)
    
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado.")

    for key, value in recinto_data.model_dump(exclude_unset=True).items():
        setattr(recinto, key, value)

    session.add(recinto)
    session.commit()
    session.refresh(recinto)
    
    return recinto

# Eliminar Recinto
@router.delete("/{id_recinto}", status_code=204)
def delete_recinto(id_recinto: int, session: Session = Depends(get_session)):
    
    recinto = session.get(Recinto, id_recinto)
    
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado.")

    session.delete(recinto)
    session.commit()
    

