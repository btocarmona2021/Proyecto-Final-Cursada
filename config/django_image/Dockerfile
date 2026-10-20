FROM python:3.12

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc

ARG UID=500
ARG GID=500

RUN if ! getent group "${GID}" > /dev/null; then \
        groupadd -g "${GID}" appuser; \
    fi && \
    if ! getent passwd "${UID}" > /dev/null; then \
        useradd -u "${UID}" -g "${GID}" -m appuser; \
    fi

# Asignar al UID y GID indicados la carpeta de trabajo.
RUN mkdir -p /home/appuser/app && chown -R "${UID}:${GID}" /home/appuser

WORKDIR /home/appuser/app

RUN pip install --upgrade pip setuptools

COPY requirements.txt .

RUN pip install -r requirements.txt

# Ejecutar el backend con el UID y GID indicados.
USER ${UID}:${GID}

EXPOSE 8001

CMD python manage.py runserver 0.0.0.0:8001
