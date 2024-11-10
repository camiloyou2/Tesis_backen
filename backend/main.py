from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from  dotenv import load_dotenv
from routes.auth import auth_routes 
from routes.grant_user import grants_user_routes
from routes.power import api_power
app = FastAPI()

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permite solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
app.include_router(auth_routes, prefix="/api")
app.include_router(grants_user_routes, prefix="/user")
app.include_router(api_power, prefix="/power")
load_dotenv()

