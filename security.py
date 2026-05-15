import os
import bcrypt
from dotenv import load_dotenv

# Cargar variables de entorno (donde está el Pepper)
load_dotenv()

def get_pepper() -> bytes:
    pepper = os.getenv("PEPPER_SECRET")
    if not pepper:
        raise ValueError("PEPPER_SECRET no está configurado en las variables de entorno.")
    return pepper.encode('utf-8')

def get_password_hash(password: str) -> str:
    """
    Toma la contraseña en texto plano, le concatena el Pepper y genera el Hash.
    El Salt es generado explícitamente y utilizado por bcrypt.
    """
    peppered_password = password.encode('utf-8') + get_pepper()
    
    # Generamos un Salt aleatorio (Bcrypt maneja el factor de costo internamente, default 12)
    salt = bcrypt.gensalt()
    
    # Calculamos el hash usando la contraseña salpimentada y el salt generado
    hashed_password = bcrypt.hashpw(peppered_password, salt)
    
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña ingresada (tras aplicarle el Pepper) coincida con el Hash almacenado.
    """
    peppered_password = plain_password.encode('utf-8') + get_pepper()
    
    # checkpw se encarga de extraer el salt del hashed_password y validar
    return bcrypt.checkpw(peppered_password, hashed_password.encode('utf-8'))
