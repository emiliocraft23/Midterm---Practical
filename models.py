from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine

# Base de datos SQLite local
import os

DB_PATH = os.getenv("DB_PATH", "./users.db")

# Base de datos SQLite — en Docker usa el volumen /app/data/users.db
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


class User(SQLModel, table=True):
    """Modelo de usuario con datos cifrados y contraseña hasheada."""
    id: Optional[int] = Field(default=None, primary_key=True)

    # Almacenados cifrados con AES (encrypt_data / decrypt_data)
    username: str = Field(description="Nombre de usuario cifrado con AES")
    email: Optional[str] = Field(default=None, description="Email cifrado con AES")

    # Almacenado hasheado con bcrypt + pepper
    hashed_password: str = Field(description="Contraseña hasheada con bcrypt+pepper")

    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(SQLModel, table=True):
    """Perfil extendido del usuario."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    bio: Optional[str] = Field(default=None)
    avatar_path: Optional[str] = Field(default=None)
    is_adult: bool = Field(default=False)
    birthdate: Optional[str] = Field(default=None, description="Fecha de nacimiento YYYY-MM-DD")


def create_db_and_tables():
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)
