FROM python:3.12

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc

ARG UID=500
ARG GID=500

RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g appuser -m appuser

# Crear carpeta y asignar permisos CORRECTAMENTE
RUN mkdir -p /home/appuser/app && chown -R appuser:appuser /home/appuser

WORKDIR /home/appuser/app

RUN pip install --upgrade pip setuptools

COPY requirements.txt .

RUN pip install -r requirements.txt

# Cambiar al usuario recién acá
USER appuser

EXPOSE 8001

CMD python manage.py runserver 0.0.0.0:8001