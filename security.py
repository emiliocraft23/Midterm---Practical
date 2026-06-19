import os
import bcrypt
import base64

from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Configuración: se leen desde el archivo .env
# ──────────────────────────────────────────────────────────────────────────────

PEPPER: str = os.getenv("PEPPER", "")
AES_KEY: bytes = os.getenv("AES_KEY", "").encode()

if not PEPPER:
    raise RuntimeError("La variable de entorno PEPPER no está definida en .env")

if len(AES_KEY) not in (16, 24, 32):
    raise RuntimeError(
        f"AES_KEY debe tener 16, 24 o 32 bytes. Tiene {len(AES_KEY)}."
    )


# ──────────────────────────────────────────────────────────────────────────────
# Hashing de contraseñas con bcrypt + pepper
# ──────────────────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt con pepper.

    Flujo:
        1. Se concatena la contraseña con el PEPPER.
        2. Se genera un salt aleatorio con bcrypt.
        3. Se hashea la combinación password+pepper.
        4. Se devuelve el hash como string.

    Args:
        password: Contraseña en texto plano ingresada por el usuario.

    Returns:
        Hash de la contraseña listo para guardar en la base de datos.
    """
    password_with_pepper = password + PEPPER

    hashed = bcrypt.hashpw(
        password_with_pepper.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        password: Contraseña ingresada por el usuario al iniciar sesión.
        hashed_password: Hash almacenado en la base de datos.

    Returns:
        True si la contraseña es correcta, False en caso contrario.
    """
    password_with_pepper = password + PEPPER

    return bcrypt.checkpw(
        password_with_pepper.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ──────────────────────────────────────────────────────────────────────────────
# Cifrado simétrico AES-CBC para datos sensibles (email, nombre, etc.)
# ──────────────────────────────────────────────────────────────────────────────

def encrypt_data(data: str) -> str:
    """
    Cifra un string usando AES en modo CBC.

    El resultado tiene el formato: "<iv_base64>:<datos_cifrados_base64>"
    El IV (vector de inicialización) se genera aleatoriamente en cada llamada,
    lo que garantiza que el mismo dato produzca resultados distintos.

    Args:
        data: Texto plano a cifrar.

    Returns:
        String cifrado en formato "iv:ciphertext" codificado en base64.
    """
    cipher = AES.new(AES_KEY, AES.MODE_CBC)

    encrypted = cipher.encrypt(
        pad(data.encode("utf-8"), AES.block_size)
    )

    iv_b64 = base64.b64encode(cipher.iv).decode("utf-8")
    encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

    return f"{iv_b64}:{encrypted_b64}"


def decrypt_data(encrypted_data: str) -> str:
    """
    Descifra un string previamente cifrado con encrypt_data().

    Args:
        encrypted_data: String en formato "iv_base64:datos_base64".

    Returns:
        Texto original descifrado.

    Raises:
        ValueError: Si el formato del string cifrado es inválido.
    """
    if ":" not in encrypted_data:
        raise ValueError("Formato de datos cifrados inválido. Se esperaba 'iv:ciphertext'.")

    iv_b64, encrypted_b64 = encrypted_data.split(":", 1)

    iv = base64.b64decode(iv_b64)
    encrypted_bytes = base64.b64decode(encrypted_b64)

    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)

    decrypted = unpad(
        cipher.decrypt(encrypted_bytes),
        AES.block_size
    )

    return decrypted.decode("utf-8")
