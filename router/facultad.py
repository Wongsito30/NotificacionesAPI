from fastapi import APIRouter
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.modelos as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_Msgfacultad():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verNotificacionesFacultad/", response_model=List[page_schemas.facultad])
async def show_notiFacul(db:session=Depends(get_Msgfacultad)):
    notificacion = db.query(page_models.Facultad).all()
    return notificacion

@router.post("/registrarNotificacionesFacultad/",response_model=page_schemas.facultad)
def create_notifacul(entrada:page_schemas.facultad,db:session=Depends(get_Msgfacultad)):
    usuario = page_models.Facultad(fecha = entrada.fecha,mensaje = entrada.mensaje)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.put("/CambiarMensajeFacultad/{Notificacion_id}",response_model=page_schemas.facultad)
def mod_noti_facul(notiid: int, entrada:page_schemas.facultad,db:session=Depends(get_Msgfacultad)):
    NotiFacul = db.query(page_models.Facultad).filter_by(id=notiid).first()
    NotiFacul.fecha = entrada.fecha
    NotiFacul.mensaje = entrada.mensaje

    db.commit()
    db.refresh(NotiFacul)
    return NotiFacul

@router.delete("/EliminarNotificacionFacultad/{noti_id}",response_model=page_schemas.respuesta)
def del_Noti_Facul(Notiid: int,db:session=Depends(get_Msgfacultad)):
    Notifacul = db.query(page_models.Facultad).filter_by(id=Notiid).first()
    db.delete(Notifacul)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta