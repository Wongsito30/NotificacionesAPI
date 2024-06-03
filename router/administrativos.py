from fastapi import APIRouter, Query
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from sqlalchemy import create_engine, asc, desc, func
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

@router.get("/verAdministrativos/")
async def show_Administrativos(db: session = Depends(get_MsgAdministrativos)):
    administrativos = db.query(page_models.Personaladmin).all()
    return {"administrativos": [admin.admin for admin in administrativos]}

@router.get("/searchNotiNombreAdmin/{adminname}", response_model=List[page_schemas.personaladministrativo])
async def show_NotiNomCarrera(adminname: str, db: session = Depends(get_MsgAdministrativos)):
    # Filtra las notificaciones que coinciden con el nombre
    noti = db.query(page_models.Personaladmin).filter(func.lower(page_models.Personaladmin.admin).ilike(f"%{adminname}%")).all()
    return noti

@router.get("/notificacion/fechaasc", response_model=List[page_schemas.personaladministrativo])
async def get_noti_ascending(
    db: session = Depends(get_MsgAdministrativos),
    field: str = Query("fecha")
):
    if field not in page_models.Personaladmin.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de menor a mayor
    noti = db.query(page_models.Personaladmin).order_by(asc(field)).all()
    return noti

@router.get("/notificacion/fechadesc", response_model=List[page_schemas.personaladministrativo])
async def get_noti_descending(
    db: session = Depends(get_MsgAdministrativos),
    field: str = Query("fecha")
):
    if field not in page_models.Personaladmin.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de mayor a menor
    noti = db.query(page_models.Personaladmin).order_by(desc(field)).all()
    return noti

@router.post("/registrarNotificacionesAdministrativos/",response_model=page_schemas.personaladministrativo)
def create_notiAdministrativos(entrada:page_schemas.personaladministrativo,db:session=Depends(get_MsgAdministrativos)):
    notificacion = page_models.Personaladmin(admin = entrada.admin, fecha = entrada.fecha,mensaje = entrada.mensaje)
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.put("/CambiarMensajeAdministrativos/{Notificacion_id}",response_model=page_schemas.personaladministrativo)
def mod_noti_Administrativos(notiid: int, entrada:page_schemas.personaladministrativo,db:session=Depends(get_MsgAdministrativos)):
    NotiAdministrativos = db.query(page_models.Personaladmin).filter_by(id=notiid).first()
    NotiAdministrativos.admin = entrada.admin
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