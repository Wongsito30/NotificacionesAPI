from fastapi import APIRouter
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from passlib.context import CryptContext
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.modelos as page_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_admin():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verAdmin/", response_model=List[page_schemas.Admin])
async def show_Admin(db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).all()
    return admin

@router.post("/registrarAdmin/",response_model=page_schemas.Admin)
def create_admin(entrada:page_schemas.Admin,db:session=Depends(get_admin)):
   hashed_password = pwd_context.hash(entrada.contrasena)
   #codigo1 = random.randint(1000, 9999)
   admin = page_models.Admin(admin = entrada.admin,contrasena = hashed_password)
   db.add(admin)
   db.commit()
   db.refresh(admin)
   return admin

@router.put("/CambiarAdmin/{Admin_id}",response_model=page_schemas.Admin)
def mod_admin(adminid: int, entrada:page_schemas.Admin,db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).filter_by(id=adminid).first()
    admin.admin = entrada.admin
    admin.contrasena = entrada.contrasena
    db.commit()
    db.refresh(admin)
    return admin

@router.delete("/EliminarAdmin/{Admin_id}",response_model=page_schemas.respuesta)
def del_Admin(Adminid: int,db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).filter_by(id=Adminid).first()
    db.delete(admin)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta