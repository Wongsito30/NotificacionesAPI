from sqlalchemy import Column, Integer, String, LargeBinary, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    contrasena =  Column(String(16))
    nombrecarrera = Column(String(150))
    grupo = Column(String(5))
    administrativo = Column(String(3))

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    admin = Column(String(16))
    contrasena =  Column(String(16))

class Carreras(Base):
    __tablename__ = 'carrera'

    id = Column(Integer, primary_key=True, index=True)
    nombrecarrera = Column(String(150))
    fecha = Column(String(Date))
    mensaje =  Column(String(500))

class Facultad(Base):
    __tablename__ = 'facultad'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    mensaje =  Column(String(500))


class Grupos(Base):
    __tablename__ = 'grupo'

    id = Column(Integer, primary_key=True, index=True)
    nombrecarrera = Column(String(150))
    grupo = Column(String(5))
    fecha = Column(String(Date))
    mensaje =  Column(String(500))

class Personaladmin(Base):
    __tablename__ = 'personaladministrativo'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String(Date))
    mensaje =  Column(String(500))