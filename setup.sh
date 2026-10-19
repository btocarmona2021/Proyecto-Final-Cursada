#!/bin/bash

UID_VAL=$(id -u)
GID_VAL=$(id -g)

# Crea o sobrescribe el .env.user con los valores de tu usuario
cat > .env.user << EOF
UID=${UID_VAL}
GID=${GID_VAL}
EOF

echo "✓ Archivo .env.user generado exitosamente con UID=${UID_VAL} y GID=${GID_VAL}"

docker compose --env-file .env --env-file .env.user up -d --build