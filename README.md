# Proyecto Final — Sistema de Gestión Veterinaria

## Sobre el repositorio

Este repositorio tiene dos etapas bien diferenciadas:

| Etapa | Commits | Descripción |
|-------|---------|-------------|
| Proyecto inicial | `30f0d1c` → `ee37c11` | Primer proyecto, estructura monolítica en Django |
| Transición | `0d0d9ad` | Reinicio: cambio de proyecto y tecnología |
| Proyecto final | `a19ccd3` en adelante | Sistema de Gestión Veterinaria — Django REST + Vue 3 |

El cambio de rumbo fue intencional: comencé con otro enfoque y luego decidí replantear el proyecto desde cero con una arquitectura más sólida (API REST + SPA). El commit `0d0d9ad` marca esa ruptura eliminando el código viejo y `a19ccd3` introduce el código nuevo completo.

## Stack actual

- **Backend**: Django + Django REST Framework + Simple JWT + PostgreSQL
- **Frontend**: Vue 3 + TypeScript + Pinia + Bootstrap 5
- **Infra**: Docker + Docker Compose

## Ejecutar

```bash
docker compose up -d --build
```
