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


def get_MsgCarreras():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verNotificacionesCarreras/", response_model=List[page_schemas.carrera])
async def show_notiCarrera(db:session=Depends(get_MsgCarreras)):
    notificacion = db.query(page_models.Carreras).all()
    return notificacion

@router.post("/registrarNotificacionesCarreras/",response_model=page_schemas.carrera)
def create_notiCarrera(entrada:page_schemas.carrera,db:session=Depends(get_MsgCarreras)):
    notificacion = page_models.Carreras(nombrecarrera = entrada.nombrecarrera ,fecha = entrada.fecha,mensaje = entrada.mensaje)
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.put("/CambiarMensajeCarrera/{Notificacion_id}",response_model=page_schemas.carrera)
def mod_noti_carrera(notiid: int, entrada:page_schemas.carrera,db:session=Depends(get_MsgCarreras)):
    NotiCarrera = db.query(page_models.Carreras).filter_by(id=notiid).first()
    NotiCarrera.nombrecarrera = entrada.nombrecarrera
    NotiCarrera.fecha = entrada.fecha
    NotiCarrera.mensaje = entrada.mensaje

    db.commit()
    db.refresh(NotiCarrera)
    return NotiCarrera

@router.delete("/EliminarNotificacionCarrera/{noti_id}",response_model=page_schemas.respuesta)
def del_Noti_Carreras(Notiid: int,db:session=Depends(get_MsgCarreras)):
    NotiCarrera = db.query(page_models.Carreras).filter_by(id=Notiid).first()
    db.delete(NotiCarrera)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta