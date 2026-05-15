# 🐾 Sistema de Gestión Veterinaria – API Backend

Backend del sistema de gestión veterinaria para clínica pequeña/mediana.  
Tecnologías: **Django 6 + Django REST Framework + Simple JWT + PostgreSQL**. [file:14][web:141]

---

## 1. Autenticación y roles

### 1.1. Autenticación

- Mecanismo: **JWT** (`djangorestframework-simplejwt`). [file:14][web:130]
- Flujo típico:
  - `POST /api/token/` → obtiene `access` y `refresh`.
  - `POST /api/token/refresh/` → renueva `access`.
- Header:
  - `Authorization: Bearer <access_token>`. [web:131]

### 1.2. Grupos / Roles

Se usan **grupos nativos de Django** (`django.contrib.auth.models.Group`) para RBAC. [web:26][file:100]

- `clientes`: dueños de mascotas.
- `veterinarios`: personal médico.
- `admin`: administradores (usuarios `is_staff=True`).

Asignación de grupos:
- En registro de cliente: se agrega automáticamente al grupo `clientes`. [file:99]
- En registro de veterinario: se agrega al grupo `veterinarios`. [file:99]
- Admin se define desde el panel / shell como `is_staff` / `superuser`. [web:24]

---

## 2. Permisos (core/permissions.py)

Toda la lógica de permisos está centralizada en `core/permissions.py`. [file:103][web:1]

### 2.1. Clases de permisos principales

- `IsCliente`
  - `has_permission`: usuario pertenece al grupo `clientes`. [file:103]
- `IsVeterinario`
  - `has_permission`: usuario en grupo `veterinarios`. [file:103]
- `IsVeterinarioOrAdmin`
  - `has_permission`: `user.is_staff` o grupo `veterinarios`. [file:103]
- `IsAdminUser`
  - `has_permission`: `user.is_staff`. [file:103]
- `ReadOnly`
  - Permite solo métodos seguros (`GET`, `HEAD`, `OPTIONS`). [web:1][file:103]

### 2.2. Permisos por dominio

- `CanManageMascota`
  - GET: todos (filtrado en `get_queryset`). [file:102][file:103]
  - POST: solo veterinarios/admins.
  - PUT/PATCH/DELETE: dueño de la mascota o staff.
  - Usa `has_object_permission` para validar que `obj.usuario == request.user`. [file:103]

- `CanManageTurno`
  - GET/POST: permitidos para autenticados (reglas adicionales en view/serializer). [file:103]
  - PUT/PATCH/DELETE: solo veterinarios/admins.
  - `has_object_permission`: clientes no pueden editar/eliminar turnos. [file:103]

- `CanCancelTurno`
  - Clientes pueden cancelar **sus** turnos.
  - Veterinarios/admins pueden cancelar cualquier turno. [file:103]

- `CanManageEspecieRaza`
  - GET: todos (catálogo).
  - POST/PUT/PATCH/DELETE: solo admins. [file:103]

- `CanManageServicio`
  - GET: todos.
  - POST/PUT/PATCH/DELETE: solo admins. [file:103]

- `CanManageVeterinarioPerfil`
  - GET: todos.
  - POST/PUT/PATCH/DELETE: solo admins. [file:103]

- Genéricos reutilizables:
  - `IsOwnerOrReadOnly`: lectura todos, escritura dueño o staff (requiere campo `usuario`). [file:103]
  - `IsOwnerOrStaff`: dueño o staff (sin distinción de método). [file:103]

---

## 3. Matriz de permisos (resumen funcional)

### 3.1. Mascotas

| Acción                 | Cliente                      | Veterinario           | Admin            |
|------------------------|-----------------------------|-----------------------|------------------|
| Ver listado            | Solo sus mascotas           | Todas                 | Todas            |
| Ver detalle            | Solo sus mascotas           | Todas                 | Todas            |
| Crear mascota          | No (bloqueado por permiso)  | Sí                    | Sí               |
| Editar mascota         | Solo sus mascotas           | Cualquiera            | Cualquiera       |
| Eliminar (DELETE)      | Solo sus mascotas (si lo usas) | Cualquiera        | Cualquiera       |

Implementado vía:
- `MascotaViewSet` + `CanManageMascota` + `get_queryset` filtrando por dueño. [file:102][file:103]

### 3.2. Turnos

| Acción                 | Cliente                               | Veterinario            | Admin                    |
|------------------------|----------------------------------------|------------------------|--------------------------|
| Ver listado            | Solo turnos de sus mascotas           | Todos                  | Todos                    |
| Ver detalle            | Solo turnos de sus mascotas           | Todos                  | Todos                    |
| Crear turno            | Solo para sus mascotas (validación)   | Cualquier mascota      | Cualquier mascota        |
| Editar turno           | No (bloqueado)                        | Sí                     | Sí                       |
| Eliminar turno         | No (bloqueado)                        | Sí                     | Sí                       |
| Cancelar turno         | Solo sus turnos                       | Cualquier turno        | Cualquier turno          |

Implementado vía:  
- `TurnoViewSet` + `CanManageTurno` + lógica en `perform_create` y `get_queryset`. [file:102][file:103][file:99]

### 3.3. Consultas, internaciones y vacunas

| Recurso          | Cliente                             | Veterinario / Admin         |
|------------------|--------------------------------------|-----------------------------|
| Consultas        | Ver solo consultas de sus mascotas   | CRUD completo               |
| Internaciones    | No gestiona                          | CRUD completo               |
| Evoluciones      | No gestiona                          | CRUD completo               |
| Vacunas          | Ver vacunas de sus mascotas          | CRUD completo               |

Implementado vía:
- Filtros por `mascota__usuario=user` en `get_queryset` cuando `user` es cliente. [file:102]
- Uso de `IsVeterinarioOrAdmin` en operaciones de escritura. [file:102][file:103]

---

## 4. Endpoints principales

Los paths exactos dependen de tus `routers`, pero a nivel recurso:

### 4.1. Usuarios / Perfiles

**Usuarios (solo lectura)**  
- `GET /api/usuarios/`
- `GET /api/usuarios/{id}/`  
  - `UsuarioViewSet` (ReadOnlyModelViewSet, `IsAuthenticated`). [file:102][web:59]

**Clientes (perfil)**  
- `POST /api/clientes/`  
  - Registro de cliente (público, `AllowAny`).  
  - Crea `User`, asigna grupo `clientes`, crea `PerfilUsuario`. [file:99][file:102]
- `GET /api/clientes/`  
- `GET /api/clientes/{id}/`  
- `PUT/PATCH/DELETE /api/clientes/{id}/`  
  - Requiere autenticación. [file:102]

**Veterinarios**  
- `POST /api/veterinarios/`  
  - Solo admin (`IsAdminUser`). Crea `User` + `VeterinarioPerfil`. [file:99][file:102]
- `GET /api/veterinarios/`
- `GET /api/veterinarios/{id}/`
- `PUT/PATCH/DELETE /api/veterinarios/{id}/`  
  - Autenticado, permisos según vista. [file:102]

**Horarios de Veterinarios**  
- `GET /api/horarios-veterinario/`
- `POST /api/horarios-veterinario/`
- `PUT/PATCH/DELETE /api/horarios-veterinario/{id}/`  
  - `HorarioVeterinarioViewSet` con `IsVeterinarioOrAdmin`. [file:102][file:103]

Validaciones de horarios:
- `HorarioVeterinarioSerializer.validate` impide solapamiento de horarios para el mismo vet/día. [file:99]

### 4.2. Mascotas, Especies y Razas

**Especies**  
- `GET /api/especies/` → lista de especies activas. [file:102]
- `POST/PUT/PATCH/DELETE /api/especies/` → solo admin (`CanManageEspecieRaza`). [file:103]

**Razas**  
- `GET /api/razas/?especie_id={id}` → razas filtradas por especie. [file:102]
- Mutaciones: solo admin (`CanManageEspecieRaza`). [file:103]

**Mascotas**  
- `GET /api/mascotas/`  
  - Clientes: solo sus mascotas (filtro en `get_queryset`). [file:102]
  - Vet/Admin: todas. [file:102]
- `GET /api/mascotas/{id}/`
- `POST /api/mascotas/`  
  - Solo vet/admin (por `CanManageMascota` y validación de grupo en `MascotaCreateSerializer`). [file:99][file:103]
- `PUT/PATCH/DELETE /api/mascotas/{id}/`  
  - Dueño o staff. [file:102][file:103]

Validaciones de mascotas:
- `MascotaCreateSerializer.validate` → el usuario dueño debe pertenecer al grupo Cliente (ajustar nombre de grupo a `clientes`). [file:99]
- Cálculo de edad por `fecha_nacimiento`. [file:99]

### 4.3. Turnos (agenda)

Recurso `Turno` y `Servicio`. [file:99][file:102]

**Servicios**  
- `GET /api/servicios/` → catálogo de servicios.  
- Mutaciones: solo admin (`CanManageServicio`). [file:103]

**Turnos** (`TurnoViewSet`)  
- `GET /api/turnos/`
  - Clientes: solo turnos de sus mascotas. [file:102]
  - Vet/Admin: todos. [file:102]
  - Filtros por query params:
    - `estado`
    - `mascota_id`
    - `veterinario_id`
    - `usuario_id` (dueño). [file:102]
- `POST /api/turnos/`
  - Clientes: solo para SUS mascotas.
  - Vet/Admin: cualquier mascota. [file:102]

**Validaciones de negocio en TurnoCreateSerializer**: [file:99]

1. **Fecha futura**
   ```python
   def validate_fecha_hora(self, value):
       from django.utils import timezone
       if value < timezone.now():
           raise serializers.ValidationError(
               "La fecha del turno debe ser futura"
           )
       return value
   ```

2. **Horario del veterinario**
   - Usa `HorarioVeterinario`:
     - Mismo vet.
     - `dia_semana` coincide (`isoweekday()`).
     - `hora_inicio <= hora <= hora_fin`.
     - `activo=True`. [file:99]
   - Error:
     - `"El veterinario no atiende en ese día y horario."`

3. **Solapamiento de turnos**
   - Calcula `duracion = timedelta(minutes=servicio.duracion_estimada)`.
   - Ventana: `[fecha_hora - duracion, fecha_hora + duracion]`.
   - Filtra turnos del mismo vet con `estado` en:
     `"reservado", "confirmado", "en_espera", "en_consulta"`. [file:99]
   - Excluye `self.instance` si es update. [file:99]
   - Error:
     - `"El veterinario ya tiene un turno en ese horario."`

**Seguridad adicional en TurnoViewSet**: [file:102][file:103]

- `get_queryset`:
  - Clientes → `filter(mascota__usuario=user)`.
- `perform_create`:
  - Clientes → si `mascota.usuario != user` → `PermissionDenied("No puede crear turnos para mascotas que no son suyas.")`.
  - Marca `creado_por_cliente=True` cuando corresponde. [file:102]
- `perform_update` / `perform_destroy`:
  - Bloquean edición/eliminación a clientes (solo vet/admin).

### 4.4. Historia clínica

Endpoints principales:

- `ConsultaClinicaViewSet`
  - `GET /api/consultas/`:
    - Clientes: solo consultas de sus mascotas (filtro por `mascota__usuario=user`). [file:102]
    - Vet/Admin: todas.
  - `POST/PUT/PATCH/DELETE`:
    - Solo vet/admin (`IsVeterinarioOrAdmin` en `get_permissions`). [file:102][file:103]

- `RecetaItemViewSet`
  - CRUD completo para recetas, restringido a vet/admin (`IsVeterinarioOrAdmin`). [file:102]

- `VacunaViewSet`
  - `GET`: clientes ven vacunas de sus mascotas; vet/admin todas. [file:102]
  - Mutaciones: solo vet/admin (`get_permissions` con `IsVeterinarioOrAdmin`). [file:102]

### 4.5. Internaciones

- `InternacionViewSet`
  - CRUD completo para internaciones.
  - Solo vet/admin (`IsVeterinarioOrAdmin`). [file:102][file:103]
  - Filtro opcional por `estado`. [file:102]

- `EvolucionInternacionViewSet`
  - CRUD de evoluciones ligadas a internación.
  - Solo vet/admin (`IsVeterinarioOrAdmin`). [file:102]

---

## 5. Notificaciones

- `NotificacionViewSet`
  - `GET /api/notificaciones/`:
    - Devuelve **solo notificaciones del usuario autenticado** (`filter(usuario=self.request.user)`). [file:102]
    - Filtro opcional `leida=true|false`. [file:102]
  - `POST/PUT/PATCH/DELETE`:
    - Internamente usás `IsAuthenticated`; el control fine-grained se hace en la lógica de negocio según quién crea las notificaciones. [file:102]

- `NotificacionSerializer.update`
  - Si `leida` pasa de `False` a `True` → setea `fecha_lectura = timezone.now()`. [file:99]
  - Si se desmarca `leida` → limpia `fecha_lectura`. [file:99]

---

## 6. Datos de la clínica

- `VeterinariaViewSet`
  - `GET /api/clinica/`:
    - Info general de la clínica (nombre, dirección, horarios, redes). [file:100][file:102]
  - Mutaciones:
    - Solo admin (`IsAdminUser` en `get_permissions`). [file:102][file:103]
  - Modelo restringe a una sola clínica (lanza error si se intenta crear más de una). [file:100]

---

## 7. Notas finales para el evaluador

- Seguridad:
  - Autenticación JWT en todos los endpoints protegidos.
  - Permisos centralizados en `core/permissions.py`.
  - Filtrado por rol/propietario en `get_queryset` para clientes. [file:102][file:103]
- Negocio:
  - Turnos respetan horarios de veterinarios y evitan solapamientos.
  - Clientes no pueden operar sobre recursos que no les pertenecen (mascotas, turnos, historia clínica).
- Mantenibilidad:
  - ViewSets limpios gracias a permisos reutilizables.
  - Serializers separados para creación vs lectura cuando es útil (mascotas, turnos). [file:99][web:59]

Este README resume la estructura y comportamiento del backend de la veterinaria y sirve como documentación técnica para el proyecto final.
