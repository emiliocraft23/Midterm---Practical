from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import create_db_and_tables
from routes.auth_routes import router as auth_router

# ──────────────────────────────────────────────────────────────────────────────
# Aplicación principal
# ──────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="API de Seguridad - Usuarios",
    description=(
        "API REST para registro e inicio de sesión de usuarios con:\n"
        "- **bcrypt + pepper** para hashing de contraseñas\n"
        "- **AES-CBC** para cifrado simétrico de datos sensibles (username, email)"
    ),
    version="1.0.0",
)

# CORS: permite peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Cambiar a la URL del frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al arrancar
create_db_and_tables()

# Registrar rutas de autenticación
app.include_router(auth_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "API de Seguridad funcionando correctamente.",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /auth/register",
            "login":    "POST /auth/login",
            "users":    "GET  /auth/users  (debug)"
        }
    }
