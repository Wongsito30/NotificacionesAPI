from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import login
from router import usuarios
from router import admin
from router import administrativos
from router import carrera
from router import facultad
from router import grupos
from router import loginadmin


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login.router, tags=["login"])
app.include_router(loginadmin.router, tags=["login admin"])
app.include_router(usuarios.router, tags=["Usuarios Crud"])
app.include_router(admin.router, tags=["admin crud"])
app.include_router(administrativos.router, tags=["notificaciones administrativos"])
app.include_router(carrera.router, tags=["notificaciones carrera"])
app.include_router(facultad.router, tags=["notificaciones facultad"])
app.include_router(grupos.router, tags=["grupos"])


@app.get("/")
async def root():
    return {"message": "Hello World"}