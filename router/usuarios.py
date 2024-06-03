from fastapi import APIRouter
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
from passlib.context import CryptContext
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.modelos as page_models
import random
import yagmail

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_Users():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verUsers/", response_model=List[page_schemas.User])
async def show_User(db:session=Depends(get_Users)):
    Users = db.query(page_models.Usuarios).all()
    return Users

@router.post("/registrarUsers/",response_model=page_schemas.User)
def create_user(entrada:page_schemas.User,db:session=Depends(get_Users)):
    hashed_password = pwd_context.hash(entrada.contrasena)
    #codigo1 = random.randint(1000, 9999)
    usuario = page_models.Usuarios(nickname = entrada.nickname,contrasena = hashed_password, nombrecarrera = entrada.nombrecarrera, grupo = entrada.grupo)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.put("/CambiarUsersadmin/{usuario_id}",response_model=page_schemas.User)
def mod_user_admin(usuarioid: int, entrada:page_schemas.User,db:session=Depends(get_Users)):
    hashed_password = pwd_context.hash(entrada.contrasena)
    usuario = db.query(page_models.Usuarios).filter_by(id=usuarioid).first()
    usuario.nickname = entrada.nickname
    usuario.contrasena = hashed_password
    usuario.nombrecarrera = entrada.nombrecarrera
    usuario.grupo = entrada.grupo
    usuario.administrativo = entrada.administrativo
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/EliminarUsers/{usuario_id}",response_model=page_schemas.respuesta)
def del_user(usuarioid: int,db:session=Depends(get_Users)):
    usuario = db.query(page_models.Usuarios).filter_by(id=usuarioid).first()
    db.delete(usuario)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta