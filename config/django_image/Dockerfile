#FARPICEC
FROM python:3.12

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc

ARG UID=500
ARG GID=500

RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g appuser -m appuser

# Uso el home del usuario en vez de /usr/src/app ya que el propietario de usr en el contendedor siempre sera root
WORKDIR /home/appuser/app

RUN pip install --upgrade pip setuptools

COPY requirements.txt .

RUN pip install -r requirements.txt

USER appuser

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000