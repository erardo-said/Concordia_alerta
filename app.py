from fastapi import FastAPI, HTTPException, status, Query, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import math

# Inicializamos la aplicación con la ruta de documentación en castellano
app = FastAPI(
    title="Concordia Alerta API",
    description="Backend prototipo para app de seguridad comunitaria en Concordia, Entre Ríos",
    version="1.0.0",
    docs_url="/documentacion",  # Ahora entras desde /documentacion en vez de /docs
    redoc_url=None
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que cualquier pantalla web se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. MODELOS DE DATOS (Esquemas) ---

class Usuario(BaseModel):
    id: int = Field(..., description="ID único del usuario")
    nombre: str = Field(..., description="Nombre y apellido del vecino")
    telefono: str = Field(..., description="Número de teléfono de contacto")

class AlertaBase(BaseModel):
    tipo: str = Field(..., description="Ej: Robo, Actividad Sospechosa, Mascota Perdida, Incendio")
    descripcion: str = Field(..., description="Detalles o aclaraciones de la emergencia")
    latitud: float = Field(..., description="Latitud en Concordia (Aprox. -31.39)")
    longitud: float = Field(..., description="Longitud en Concordia (Aprox. -58.02)")
    usuario_id: int = Field(..., description="ID del usuario que reporta el incidente")

class AlertaRespuesta(AlertaBase):
    id: int
    fecha_creacion: datetime = Field(..., description="Fecha y hora exacta del reporte")

# --- 2. BASE DE DATOS TEMPORAL (Simulada en Memoria) ---
BASE_DATOS_USUARIOS = []
BASE_DATOS_ALERTAS = []

# --- 3. FUNCIONES AUXILIARES ---
def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos coordenadas usando Haversine."""
    R = 6371.0  
    rad_lat1, rad_lon1 = math.radians(lat1), math.radians(lon1)
    rad_lat2, rad_lon2 = math.radians(lat2), math.radians(lon2)
    dlat = rad_lat2 - rad_lat1
    dlon = rad_lon2 - rad_lon1
    a = math.sin(dlat / 2)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- 4. RUTAS DE LA API (Endpoints) ---

@app.get("/", tags=["General"], summary="Página de inicio con el Mapa")
def inicio():
    try:
        with open("mapa.html", "r", encoding="utf-8") as archivo:
            return HTMLResponse(content=archivo.read())
    except FileNotFoundError:
        return {"mensaje": "Bienvenido a Concordia Alerta API. El archivo mapa.html no se encuentra en el servidor."}

# --- ¡ESTA ERA LA FUNCIÓN QUE SE HABÍA BORRADO Y PROVOCABA EL ERROR! ---
@app.post("/usuarios/", response_model=Usuario, status_code=status.HTTP_201_CREATED, tags=["Usuarios"], summary="Registrar un nuevo usuario")
def registrar_usuario(usuario: Usuario):
    if any(u.id == usuario.id for u in BASE_DATOS_USUARIOS):
        raise HTTPException(status_code=400, detail="El ID de usuario ya está registrado.")
    BASE_DATOS_USUARIOS.append(usuario)
    return usuario

@app.post("/alertas/", response_model=AlertaRespuesta, status_code=status.HTTP_201_CREATED, tags=["Alertas"], summary="Crear una nueva alerta de emergencia")
def crear_alerta(alerta: AlertaBase):
    if not any(u.id == alerta.usuario_id for u in BASE_DATOS_USUARIOS):
        raise HTTPException(status_code=404, detail="Usuario no encontrado. Registrate primero.")
    
    nueva_alerta = AlertaRespuesta(
        id=len(BASE_DATOS_ALERTAS) + 1,
        tipo=alerta.tipo,
        descripcion=alerta.descripcion,
        latitud=alerta.latitud,
        longitud=alerta.longitud,
        usuario_id=alerta.usuario_id,
        fecha_creacion=datetime.now()
    )
    BASE_DATOS_ALERTAS.append(nueva_alerta)
    return nueva_alerta

@app.get("/alertas/cercanas/", response_model=List[AlertaRespuesta], tags=["Alertas"], summary="Listar alertas activas cerca de una ubicación")
def listar_alertas_cercanas(
    latitud: float = Query(..., description="Tu latitud actual en Concordia"), 
    longitud: float = Query(..., description="Tu longitud actual en Concordia"), 
    radio_km: float = Query(1.0, description="Radio de búsqueda a la redonda en kilómetros")
):
    alertas_filtradas = []
    for alerta in BASE_DATOS_ALERTAS:
        distancia = calcular_distancia_km(latitud, longitud, alerta.latitud, alerta.longitud)
        if distancia <= radio_km:
            alertas_filtradas.append(alerta)
    return alertas_filtradas
