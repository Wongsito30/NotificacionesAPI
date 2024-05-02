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


def get_MsgAdministrativos():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verNotificacionesAdministrativos/", response_model=List[page_schemas.personaladministrativo])
async def show_notiAdministrativos(db:session=Depends(get_MsgAdministrativos)):
    notificacion = db.query(page_models.Personaladmin).all()
    return notificacion

@router.post("/registrarNotificacionesAdministrativos/",response_model=page_schemas.personaladministrativo)
def create_notiAdministrativos(entrada:page_schemas.personaladministrativo,db:session=Depends(get_MsgAdministrativos)):
    notificacion = page_models.Personaladmin(fecha = entrada.fecha,mensaje = entrada.mensaje)
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.put("/CambiarMensajeAdministrativos/{Notificacion_id}",response_model=page_schemas.personaladministrativo)
def mod_noti_Administrativos(notiid: int, entrada:page_schemas.personaladministrativo,db:session=Depends(get_MsgAdministrativos)):
    NotiAdministrativos = db.query(page_models.Personaladmin).filter_by(id=notiid).first()
    NotiAdministrativos.fecha = entrada.fecha
    NotiAdministrativos.mensaje = entrada.mensaje

    db.commit()
    db.refresh(NotiAdministrativos)
    return NotiAdministrativos

@router.delete("/EliminarNotificacionAdministrativos/{noti_id}",response_model=page_schemas.respuesta)
def del_Noti_Administrativos(Notiid: int,db:session=Depends(get_MsgAdministrativos)):
    NotiAdministrativos = db.query(page_models.Personaladmin).filter_by(id=Notiid).first()
    db.delete(NotiAdministrativos)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta