from fastapi import APIRouter, Query
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from sqlalchemy import create_engine, asc, desc, func
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

@router.get("/vercarreras/")
async def show_carreras(db: session = Depends(get_MsgCarreras)):
    carreras = db.query(page_models.Carreras).all()
    return {"carreras": [carrera.nombrecarrera for carrera in carreras]}

@router.get("/searchNotiNombreCarrera/{carreraname}", response_model=List[page_schemas.carrera])
async def show_NotiNomCarrera(carreraname: str, db: session = Depends(get_MsgCarreras)):
    # Filtra las notificaciones que coinciden con el nombre
    noti = db.query(page_models.Carreras).filter(func.lower(page_models.Carreras.nombrecarrera).ilike(f"%{carreraname}%")).all()
    return noti

@router.get("/notificacioncarreras/fechaasc", response_model=List[page_schemas.carrera])
async def get_noti_ascending(
    db: session = Depends(get_MsgCarreras),
    field: str = Query("fecha")
):
    if field not in page_models.Carreras.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de menor a mayor
    noti = db.query(page_models.Carreras).order_by(asc(field)).all()
    return noti

@router.get("/notificacioncarreras/fechadesc", response_model=List[page_schemas.carrera])
async def get_noti_descending(
    db: session = Depends(get_MsgCarreras),
    field: str = Query("fecha")
):
    if field not in page_models.Carreras.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de mayor a menor
    noti = db.query(page_models.Carreras).order_by(desc(field)).all()
    return noti

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