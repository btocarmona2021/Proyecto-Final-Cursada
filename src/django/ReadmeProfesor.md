# 🐾 Sistema de Gestión Veterinaria – Resumen Backend

## 1. Tecnologías y objetivo

- **Stack**: Django 6, Django REST Framework, Simple JWT, PostgreSQL. [file:14][web:141]
- **Objetivo**: API REST para clínica veterinaria con roles diferenciados:
  - Clientes (dueños de mascotas).
  - Veterinarios.
  - Administradores. [file:14][file:100]

---

## 2. Autenticación y Roles

- **Autenticación**: JWT mediante `djangorestframework-simplejwt`. [file:14][web:130]
  - `POST /api/token/` → `access`, `refresh`.
  - `Authorization: Bearer <token>` en cada request. [web:131]
- **Roles (RBAC)** basados en grupos nativos de Django (`Group`): [web:26][file:100]
  - `clientes`: creados vía endpoint de registro.
  - `veterinarios`: creados vía endpoint de administración.
  - `admin`: usuarios `is_staff`.

---

## 3. Sistema de permisos (core/permissions.py)

Toda la lógica de permisos está centralizada en `core/permissions.py`. [file:103][web:1]

Permisos generales:
- `IsCliente`, `IsVeterinario`, `IsVeterinarioOrAdmin`, `IsAdminUser`, `ReadOnly`. [file:103]

Permisos por dominio:
- `CanManageMascota`  
  - GET: todos (filtrado por dueño).  
  - POST: solo vet/admin.  
  - PUT/PATCH/DELETE: dueño o staff. [file:103][file:102]
- `CanManageTurno`  
  - GET/POST: autenticados (reglas extra en view).  
  - PUT/PATCH/DELETE: solo vet/admin. [file:103][file:102]
- `CanManageEspecieRaza`, `CanManageServicio`, `CanManageVeterinarioPerfil`:  
  - GET: todos.  
  - Altas/bajas/cambios: solo admin. [file:103]

Helpers genéricos:
- `IsOwnerOrReadOnly`, `IsOwnerOrStaff` para modelos ligados a un usuario. [file:103]

---

## 4. Matriz de permisos (resumen)

**Mascotas**

| Acción       | Cliente                | Vet/Admin          |
|--------------|------------------------|--------------------|
| Ver          | Solo sus mascotas      | Todas              |
| Crear        | No                     | Sí                 |
| Editar/Borrar| Solo sus mascotas (si habilitado) | Cualquiera |

Implementado con `MascotaViewSet` + `CanManageMascota` + `get_queryset`. [file:102][file:103]

**Turnos**

| Acción     | Cliente                             | Vet/Admin             |
|------------|--------------------------------------|-----------------------|
| Ver        | Turnos de sus mascotas              | Todos                 |
| Crear      | Solo para sus mascotas              | Cualquier mascota     |
| Editar/Del | No                                   | Sí                    |
| Cancelar   | Solo sus turnos                     | Cualquier turno       |

Implementado con `TurnoViewSet` + `CanManageTurno` y lógica en `perform_create`. [file:102][file:103]

**Historia clínica / Internaciones / Vacunas**

- Clientes: solo pueden ver datos de **sus** mascotas. [file:102]
- Veterinarios/Admin: CRUD completo (via `IsVeterinarioOrAdmin`). [file:102][file:103]

---

## 5. Endpoints principales

### Usuarios y perfiles

- `POST /api/clientes/`  
  - Registro público de cliente, crea `User` + `PerfilUsuario` y asigna grupo `clientes`. [file:99][file:102]
- `POST /api/veterinarios/`  
  - Solo admin, crea `User` + `VeterinarioPerfil`, grupo `veterinarios`. [file:99][file:102]
- `GET /api/usuarios/`  
  - Listado de usuarios (solo autenticados). [file:102]
- `GET/POST/... /api/horarios-veterinario/`  
  - Gestión de horarios de veterinarios, solo vet/admin para mutaciones. [file:102][file:103]

### Mascotas

- `GET /api/mascotas/`  
  - Cliente: solo sus mascotas.  
  - Vet/Admin: todas. [file:102]
- `POST /api/mascotas/`  
  - Solo vet/admin, valida que el dueño sea del grupo clientes. [file:99][file:103]

### Turnos (agenda)

- `GET /api/turnos/`  
  - Cliente: solo turnos de sus mascotas.  
  - Vet/Admin: todos, con filtros (`estado`, `mascota_id`, `veterinario_id`, `usuario_id`). [file:102]
- `POST /api/turnos/`  
  - Clientes: solo para sus mascotas (valida dueño).  
  - Vet/Admin: cualquier mascota. [file:102]

**Validaciones de negocio en `TurnoCreateSerializer`:** [file:99]

1. **Fecha futura**: no permite turnos en el pasado.  
2. **Horario del veterinario**:
   - Usa `HorarioVeterinario` (día de semana + franja horaria + `activo=True`).  
   - Error: _"El veterinario no atiende en ese día y horario."_  
3. **Solapamiento**:
   - Calcula ventana usando `duracion_estimada` del servicio.  
   - Rechaza si el vet ya tiene turno activo en esa ventana.  
   - Error: _"El veterinario ya tiene un turno en ese horario."_  

### Historia clínica e internaciones

- `GET /api/consultas/` / `GET /api/vacunas/`  
  - Cliente: solo de sus mascotas.  
  - Vet/Admin: todas. [file:102]
- Mutaciones (consultas, internaciones, evoluciones, vacunas): solo vet/admin. [file:102][file:103]

### Notificaciones

- `GET /api/notificaciones/`  
  - Devuelve solo notificaciones del usuario autenticado; filtro opcional por `leida`. [file:102]
- Actualizar `leida` actualiza automáticamente `fecha_lectura`. [file:99]

### Datos de la clínica

- `GET /api/clinica/`  
  - Información general de la veterinaria. [file:100][file:102]
- Mutaciones: solo admin. [file:102][file:103]

---

## 6. Puntos fuertes del diseño

- **Seguridad**:  
  - Autenticación JWT, permisos centralizados y filtrado estricto por rol/propietario. [file:102][file:103]
- **Negocio**:  
  - Reglas de turnos (horarios y solapamientos) implementadas y probadas con usuarios de ejemplo. [file:99][file:14]
- **Mantenibilidad**:  
  - Uso de ViewSets, serializers específicos para creación/lectura y `permissions.py` reutilizable. [file:99][file:102][web:59]

Este resumen presenta el backend listo para ser consumido por un frontend en Vue 3 en el proyecto final.