from typing import Optional
from sqlmodel import SQLModel


class UserRegister(SQLModel):
    """Esquema para registro de nuevos usuarios."""
    username: str
    email: str
    password: str
    birthdate: Optional[str] = None  # Formato: YYYY-MM-DD


class UserLogin(SQLModel):
    """Esquema para inicio de sesión."""
    username: str  # Puede ser nombre de usuario o email
    password: str


class UserResponse(SQLModel):
    """Respuesta pública del usuario (sin datos sensibles)."""
    id: int
    username: str
    email: Optional[str] = None
    is_adult: bool = False


class MessageResponse(SQLModel):
    """Respuesta genérica con mensaje."""
    message: str
