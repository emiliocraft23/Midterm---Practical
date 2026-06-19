# API de Seguridad para Usuarios

API REST construida con **FastAPI** que implementa hashing y cifrado para el manejo seguro de usuarios.

---

## 🔐 Técnicas de seguridad implementadas

| Técnica | Uso | Librería |
|---|---|---|
| **bcrypt + Pepper** | Hashing de contraseñas | `bcrypt` |
| **AES-CBC** | Cifrado de username y email | `pycryptodome` |
| **Variables de entorno** | Claves secretas fuera del código | `python-dotenv` |

---

## 📁 Estructura del proyecto

```
Final/
├── .env                  # Variables secretas (PEPPER, AES_KEY)
├── main.py               # Punto de entrada de la API
├── models.py             # Modelos de base de datos (SQLite)
├── schemas.py            # Esquemas de request/response
├── security.py           # Funciones de hashing y cifrado ⭐
├── requirements.txt      # Dependencias
└── routes/
    ├── __init__.py
    └── auth_routes.py    # Endpoints: /auth/register, /auth/login
```

---

## ⚙️ Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar el .env (editar con tus claves reales)
# PEPPER=tu_pepper_secreto
# AES_KEY=clave16caracteres    ← debe tener exactamente 16, 24 o 32 chars

# 4. Correr la API
uvicorn main:app --reload
```

La API estará disponible en: http://127.0.0.1:8000

Documentación interactiva: http://127.0.0.1:8000/docs

---

## 🚀 Endpoints

### `POST /auth/register`
Registra un nuevo usuario.

```json
{
  "username": "juan123",
  "email": "juan@ejemplo.com",
  "password": "MiClave$egura1",
  "birthdate": "2000-05-15"
}
```

**Proceso interno:**
1. Verifica que username y email no estén duplicados (descifrando los existentes).
2. Cifra `username` y `email` con AES-CBC antes de guardarlos.
3. Hashea `password` con bcrypt + PEPPER.
4. Crea el perfil y calcula automáticamente si es mayor de edad.

---

### `POST /auth/login`
Inicia sesión con username o email.

```json
{
  "username": "juan123",
  "password": "MiClave$egura1"
}
```

**Proceso interno:**
1. Recorre todos los usuarios y descifra su username/email para comparar.
2. Verifica la contraseña con `bcrypt.checkpw()` + PEPPER.
3. Devuelve los datos del usuario si las credenciales son correctas.

---

### `GET /auth/users`
Lista todos los usuarios descifrados. **Solo para desarrollo/debug.**

---

## 🔑 Explicación de `security.py`

```python
# HASHING: bcrypt + pepper
hash_password(password)        # Hashea la contraseña
verify_password(pw, hash)      # Verifica si la contraseña coincide

# CIFRADO AES-CBC
encrypt_data(data)             # Cifra un string → "iv_b64:ciphertext_b64"
decrypt_data(encrypted_data)   # Descifra el string
```

**¿Por qué pepper?**
El pepper es una cadena secreta que se añade a la contraseña *antes* de hashear.
A diferencia del salt (que se guarda en la BD), el pepper vive en el servidor.
Esto significa que aunque alguien robe la base de datos, sin el pepper no puede
realizar ataques de fuerza bruta efectivos.

**¿Por qué AES-CBC para el email/username?**
Permite recuperar el dato original (a diferencia del hash), necesario para mostrar
el email al usuario o buscar por nombre. Cada cifrado usa un IV aleatorio único.
