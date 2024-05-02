from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import login
from router import usuarios
from router import admin
from router import administrativos
from router import carrera
from router import facultad
from router import grupos


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login.router)
app.include_router(usuarios.router)
app.include_router(admin.router)
app.include_router(administrativos.router)
app.include_router(carrera.router)
app.include_router(facultad.router)
app.include_router(grupos.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}