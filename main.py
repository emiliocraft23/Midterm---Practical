from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session
from models import User, UserCreate, UserResponse
from security import get_password_hash, verify_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar la aplicación
    create_db_and_tables()
    yield
    # Se ejecuta al apagar la aplicación

app = FastAPI(title="API de Autenticación Segura", lifespan=lifespan)

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Comprobar si el usuario ya existe
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado."
        )
    
    # Hashear la contraseña (que internamente le añade el Pepper y genera un Salt)
    hashed_pwd = get_password_hash(user_data.password)
    
    # Crear el usuario y guardar en base de datos
    new_user = User(username=user_data.username, hashed_password=hashed_pwd)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@app.post("/login")
def login(user_data: UserCreate, session: Session = Depends(get_session)):
    # Buscar el usuario
    statement = select(User).where(User.username == user_data.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar contraseña
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    return {"message": "Autenticación exitosa", "user_id": user.id, "username": user.username}

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Autenticación Segura"}
