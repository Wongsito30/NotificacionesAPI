from pydantic import BaseModel
from typing import Optional
from datetime import date


class User(BaseModel):
     id: Optional[int] = None
     nickname: str
     contrasena: str
     nombrecarrera: Optional[str] = None 
     grupo: Optional[str] = None
     administrativo: Optional[str] = None

     class Config:
       from_attributes = True

class Admin(BaseModel):
     id: Optional[int] = None
     admin: str
     contrasena: str

     class Config:
       from_attributes = True  


class facultad(BaseModel):
     id: Optional[int] = None
     fecha: date
     mensaje: str
 
     class Config:
       from_attributes = True 

class carrera(BaseModel):
     id: Optional[int] = None
     nombrecarrera: str
     fecha: date
     mensaje: str
 
     class Config:
       from_attributes = True 

class grupo(BaseModel):
     id: Optional[int] = None
     nombrecarrera: str
     grupo: str
     fecha: date
     mensaje: str
 
     class Config:
       from_attributes = True 


class personaladministrativo(BaseModel):
     id: Optional[int] = None
     admin: str
     fecha: date
     mensaje: str
 
     class Config:
       from_attributes = True 

class respuesta(BaseModel):
     mensaje: str