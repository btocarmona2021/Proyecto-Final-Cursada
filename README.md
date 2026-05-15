# Proyecto Final — Sistema de Gestión Veterinaria

Aplicacion web para la gestion integral de una clinica veterinaria. Permite administrar mascotas, turnos, historia clinica, internaciones y notificaciones, con roles diferenciados para clientes, veterinarios y administradores.

## Sobre el desarrollo

El proyecto arranco con otro enfoque y sobre la marcha lo replantie por completo. Los primeros commits del repo corresponden a esa etapa inicial, y a partir de cierto punto empece de cero con una arquitectura mas solida separando backend (API REST) y frontend (SPA). El cambio fue una decision de diseño para lograr mejor organizacion y escalabilidad.

## Como levantar el proyecto

```bash
docker compose up -d --build
```

## Tecnologias usadas

- Backend: Django + Django REST Framework + Simple JWT
- Frontend: Vue 3 + TypeScript + Pinia + Bootstrap 5
- Base de datos: PostgreSQL
- Infraestructura: Docker + Docker Compose
