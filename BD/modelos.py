from sqlalchemy import Column, Integer, String, LargeBinary, Float, Date
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(length=50))
    contrasena =  Column(LONGTEXT)
    nombrecarrera = Column(String(length=150))
    grupo = Column(String(length=5))

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    admin = Column(String(length=16))
    contrasena =  Column(LONGTEXT)

class Carreras(Base):
    __tablename__ = 'carreras'

    id = Column(Integer, primary_key=True, index=True)
    nombrecarrera = Column(String(length=150))
    fecha = Column(String(Date))
    mensaje =  Column(String(length=500))

class Facultad(Base):
    __tablename__ = 'facultadnoti'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    mensaje =  Column(String(length=500))


class Grupos(Base):
    __tablename__ = 'grupos'

    id = Column(Integer, primary_key=True, index=True)
    nombrecarrera = Column(String(length=150))
    grupo = Column(String(length=5))
    fecha = Column(String(Date))
    mensaje =  Column(String(length=500))

class Personaladmin(Base):
    __tablename__ = 'personaladministrativos'

    id = Column(Integer, primary_key=True, index=True)
    admin = Column(String(length=16))
    fecha = Column(String(Date))
    mensaje =  Column(String(length=500))