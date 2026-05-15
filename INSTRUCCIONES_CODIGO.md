# API de Autenticación Segura (FastAPI + SQLModel)

Este proyecto es una implementación robusta de gestión de identidades y autenticación que utiliza técnicas avanzadas de seguridad como **Hashing**, **Salting** y **Peppering**.

## Estructura de Archivos

El proyecto está dividido en varios módulos para mantener el código ordenado (Separación de Responsabilidades):

- **`models.py`**: Contiene la definición de la base de datos (modelo `User`) y los esquemas Pydantic que sirven para validar los datos que entran y salen de los endpoints (`UserCreate`, `UserResponse`).
- **`database.py`**: Archivo de configuración de SQLModel. Se encarga de definir la conexión a la base de datos local SQLite (`auth_api.db`) y contiene la función que crea la tabla cuando la aplicación inicia.
- **`security.py`**: El corazón de la seguridad. Aquí se utiliza la librería `bcrypt`. El código incluye lógica explícita para cargar el **Pepper** desde las variables de entorno, generar un **Salt** por usuario, encriptar las contraseñas para los registros y verificarlas durante los inicios de sesión.
- **`main.py`**: El archivo principal que levanta la aplicación FastAPI. Contiene los "endpoints" o rutas (`POST /register` y `POST /login`). Además, define el evento `lifespan` que arranca la base de datos.
- **`.env`**: Archivo de entorno (oculto) que almacena tu secreto global (`PEPPER_SECRET`).
- **`informe_tecnico.md`**: El documento que te servirá de base teórica y reporte final para tu actividad.
- **`test_api.py`**: Un script de prueba escrito en Python para validar automáticamente de forma local que todo funciona correctamente.

---

## Instrucciones para Levantar el Proyecto

### 1. Activar el Entorno Virtual (Opcional, pero recomendado)
Ya se creó una carpeta `venv` con el entorno de Python. Si estás usando una consola como PowerShell en Windows, actívalo con:
```bash
.\venv\Scripts\Activate.ps1
```
*(Si usas CMD o Símbolo de sistema, usa `.\venv\Scripts\activate.bat`)*

### 2. Instalar las dependencias (Si no lo has hecho aún)
En caso de que necesites volver a instalarlas, corre el siguiente comando:
```bash
pip install -r requirements.txt
```

### 3. Iniciar el Servidor de Desarrollo
Para correr la aplicación, usa Uvicorn. Ejecuta el siguiente comando en tu terminal (asegúrate de estar en la carpeta `Partial`):
```bash
.\venv\Scripts\uvicorn main:app --reload
```
*(Alternativamente, si tienes activado tu entorno o python configurado en tu PATH, también puedes usar `python -m uvicorn main:app --reload`)*

- La etiqueta `--reload` hace que el servidor se reinicie si detecta algún cambio en el código, lo cual es muy útil mientras se desarrolla.

### 4. Probar la API (Documentación Interactiva)
FastAPI genera automáticamente documentación que puedes usar para interactuar con tus endpoints.
Abre tu navegador y entra a:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Desde allí, podrás:
1. Desplegar el bloque de **`POST /register`**.
2. Hacer clic en *"Try it out"* (Probarlo).
3. Ingresar un `username` y `password` en formato JSON y ejecutar (Execute).
4. Ver cómo la respuesta HTTP cambia a 201 Created.
5. Luego, ir a **`POST /login`** y probar a iniciar sesión con esas mismas credenciales (devolverá "Autenticación exitosa"). Si ingresas otra contraseña, te dará error "Credenciales inválidas" (401 Unauthorized).

### 5. Ver Base de Datos SQLite
A medida que interactúas con `/register`, verás que se genera un archivo `auth_api.db`.
Puedes abrir este archivo usando **DBeaver** o la extensión **SQLite Viewer** en VS Code. Podrás observar en la tabla `user` que el campo `hashed_password` contiene los hashes en lugar de contraseñas de texto claro (puedes tomar captura de esto para tu informe técnico).
