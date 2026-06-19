# ── Etapa base ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Proyecto Cybersecurity"
LABEL description="API de seguridad - hashing bcrypt + cifrado AES para usuarios"

# Evitar que Python escriba archivos .pyc y que el buffer de stdout/stderr
# cause problemas con los logs de Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero solo requirements para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Crear la carpeta de datos (la BD SQLite se guardará aquí)
RUN mkdir -p /app/data

# Exponer el puerto donde corre uvicorn
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
