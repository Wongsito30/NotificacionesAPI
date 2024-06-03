from fastapi import APIRouter, Query
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
from sqlalchemy import create_engine, asc, desc, func, and_
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.modelos as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_MsgGrupo():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verNotificacionesGrupo/", response_model=List[page_schemas.grupo])
async def show_notigrupo(db:session=Depends(get_MsgGrupo)):
    notificacion = db.query(page_models.Grupos).all()
    return notificacion

@router.get("/vergrupos/{nombreCarrera}")
async def show_grupos(nomcarrera: str, db: session = Depends(get_MsgGrupo)):
    grupos = db.query(page_models.Grupos).filter_by(nombrecarrera=nomcarrera).all()
    return {"Grupos": [Grupo.grupo for Grupo in grupos]}

@router.get("/searchNotiNombreGrupo/{carreraname}/{grupo}", response_model=List[page_schemas.grupo])
async def show_Notigrupocarrera(grupo: str, carreraname: str, db: session = Depends(get_MsgGrupo)):
    # Filtra las notificaciones que coinciden con el nombre
    noti = db.query(page_models.Grupos).filter(and_(page_models.Grupos.nombrecarrera == carreraname, page_models.Grupos.grupo == grupo)).all()
    return noti

@router.get("/notificacionGrupo/fechaasc", response_model=List[page_schemas.grupo])
async def get_noti_ascending(
    db: session = Depends(get_MsgGrupo),
    field: str = Query("fecha")
):
    if field not in page_models.Grupos.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de menor a mayor
    noti = db.query(page_models.Grupos).order_by(asc(field)).all()
    return noti

@router.get("/notificacionGrupo/fechadesc", response_model=List[page_schemas.grupo])
async def get_noti_descending(
    db: session = Depends(get_MsgGrupo),
    field: str = Query("fecha")
):
    if field not in page_models.Grupos.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de mayor a menor
    noti = db.query(page_models.Grupos).order_by(desc(field)).all()
    return noti

@router.post("/registrarNotificacionesGrupo",response_model=page_schemas.grupo)
def create_notiGrupo(entrada:page_schemas.grupo,db:session=Depends(get_MsgGrupo)):
    notificacion = page_models.Grupos(nombrecarrera = entrada.nombrecarrera, grupo = entrada.grupo ,fecha = entrada.fecha,mensaje = entrada.mensaje)
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.put("/CambiarMensajeGrupo/{Notificacion_id}",response_model=page_schemas.grupo)
def mod_noti_grupo(notiid: int, entrada:page_schemas.grupo,db:session=Depends(get_MsgGrupo)):
    Notigrupo = db.query(page_models.Grupos).filter_by(id=notiid).first()
    Notigrupo.nombrecarrera = entrada.nombrecarrera
    Notigrupo.grupo = entrada.grupo
    Notigrupo.fecha = entrada.fecha
    Notigrupo.mensaje = entrada.mensaje

    db.commit()
    db.refresh(Notigrupo)
    return Notigrupo

@router.delete("/EliminarNotificaciongrupo/{noti_id}",response_model=page_schemas.respuesta)
def del_Noti_Grupo(Notiid: int,db:session=Depends(get_MsgGrupo)):
    NotiGrupo = db.query(page_models.Grupos).filter_by(id=Notiid).first()
    db.delete(NotiGrupo)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta