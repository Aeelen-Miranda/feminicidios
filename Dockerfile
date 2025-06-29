# Usa una imagen base con las bibliotecas necesarias para geopandas
FROM python:3.10-slim

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    gcc \
    libgeos-dev \
    libproj-dev \
    libgdal-dev \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto (el mismo que usa Dash por defecto)
EXPOSE 8050

# Comando para correr la app
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050"]
