# Proyecto Final — Sistema de Gestión Veterinaria

Aplicacion web para la gestion integral de una clinica veterinaria. Permite administrar mascotas, turnos, historia clinica, internaciones y notificaciones, con roles diferenciados para clientes, veterinarios y administradores.

## Sobre el desarrollo

El proyecto arranco con otro enfoque y sobre la marcha lo replantie por completo. Los primeros commits del repo corresponden a esa etapa inicial, y a partir de cierto punto empece de cero con una arquitectura mas solida separando backend (API REST) y frontend (SPA). El cambio fue una decision de diseño para lograr mejor organizacion y escalabilidad.

## Como levantar el proyecto

Requisitos: Linux, Docker y Docker Compose.

En la primera instalación, copiar el archivo de configuración:

```bash
cp .env.example .env
```

Generar una clave para Django:

```bash
docker run --rm python:3.12 python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copiar la clave generada después de `SECRET_KEY=` en `.env`. Este archivo es local y no se sube a Git. Si ya existe, conservarlo.

Construir y levantar el frontend, el backend y la base de datos:

```bash
bash setup.sh
```

El script genera `.env.user` con el UID y GID del usuario y ejecuta Docker Compose.

Aplicar las migraciones:

```bash
docker compose --env-file .env --env-file .env.user exec backendveterinaria python manage.py migrate
```

La aplicación queda disponible en http://localhost:5173/ y la API en http://localhost:8001/api/ con los puertos de ejemplo. Una base nueva no incluye usuarios ni datos de demostración.

Para crear un administrador:

```bash
docker compose --env-file .env --env-file .env.user exec backendveterinaria python manage.py createsuperuser
```

Para comprobar TypeScript y compilar el frontend para producción:

```bash
docker compose --env-file .env --env-file .env.user exec frontend npm run build
```

## Datos de demostración

Después de aplicar las migraciones, se pueden cargar datos ficticios:

```bash
docker compose --env-file .env --env-file .env.user exec backendveterinaria python manage.py cargar_demo
```

La lógica está en `src/django/utils/datos_demo.py`. Crea una clínica si no existe, tres especies, seis razas, cuatro servicios, un veterinario con once franjas de atención, tres clientes con mascotas, cinco turnos, dos consultas con recetas, tres vacunas, dos internaciones con evoluciones y tres notificaciones.

| Rol | Usuario | Contraseña inicial |
|---|---|---|
| Administrador | `demo.admin` | `DemoAdmin123!` |
| Veterinario | `demo.veterinario` | `DemoVet123!` |
| Cliente | `demo.cliente1` | `DemoCliente123!` |
| Cliente | `demo.cliente2` | `DemoCliente123!` |
| Cliente | `demo.cliente3` | `DemoCliente123!` |

Estas cuentas son únicamente para demostración. El comando no se ejecuta automáticamente al arrancar. Repetirlo no duplica los registros creados ni restablece contraseñas. Las fechas se calculan al crear cada registro: los próximos turnos quedan para el siguiente día de lunes a viernes. Repetir la carga no reprograma los turnos existentes. Una clínica ya configurada se conserva. Si un nombre de cuenta de demostración ya pertenece a una cuenta con otra configuración, la carga se cancela sin guardar cambios.

### Vaciar los datos

Para eliminar todos los datos de la aplicación y conservar únicamente una cuenta administradora, reemplazar `NOMBRE_ADMIN` por su nombre de usuario:

```bash
docker compose --env-file .env --env-file .env.user exec backendveterinaria python manage.py vaciar_datos --administrador NOMBRE_ADMIN --confirmar
```

Esta operación elimina también los demás administradores, clientes, mascotas, turnos, historias clínicas, catálogos y datos de la clínica. Conserva la cuenta indicada, su contraseña y sus grupos, además de la estructura de la base y los permisos internos de Django. Limpia sesiones, registros de tokens y el historial del panel de administración. No elimina archivos del directorio `media`. Sin `--confirmar`, o si la cuenta indicada no es un administrador activo, no se ejecuta la eliminación. La operación se realiza en una transacción.

## Tecnologias usadas

- Backend: Django + Django REST Framework + Simple JWT
- Frontend: Vue 3 + TypeScript + Pinia + Bootstrap 5
- Base de datos: PostgreSQL
- Infraestructura: Docker + Docker Compose

## Organización

- `frontend/`: interfaz en Vue, servicios HTTP y stores de Pinia.
- `src/django/`: API y modelos de Django.
- `src/django/core/permissions.py`: permisos reutilizables.
- `config/django_image/`: imagen del backend y dependencias de Python.
- `docker-compose.yml`: servicios de frontend, backend y PostgreSQL.

El backend está dividido en usuarios, clínica, mascotas, agenda, historia clínica, internaciones y notificaciones. `core` contiene el modelo base y los permisos compartidos.

## Configuración

`.env.example` contiene las variables necesarias para crear el `.env` local. El `.env` de la raíz configura Docker y la base de datos; `frontend/.env` define `VITE_API_URL`, la dirección de la API que utiliza el navegador. La clave de Django va únicamente en el `.env` de la raíz.

`SECRET_KEY` es obligatoria y también se usa para firmar los JWT. Cambiarla invalida los tokens anteriores. `DEBUG=1` habilita el modo de desarrollo. La zona horaria de la clínica es `America/Argentina/Buenos_Aires`.

Los contenedores ejecutan los servidores de desarrollo de Django y Vite. El comando `npm run build` comprueba TypeScript y genera los archivos de producción en `frontend/dist`; no los publica ni cambia el servidor de desarrollo.

## Autenticación y roles

El login utiliza JWT:

| Método y ruta | Uso |
|---|---|
| `POST /api/token/` | Recibe `username` y `password`; devuelve tokens de acceso y renovación, datos del usuario y grupo. |
| `POST /api/token/refresh/` | Recibe `refresh` y renueva los tokens. |
| `POST /api/logout/` | Recibe `refresh` y lo agrega a la lista de tokens invalidados. Requiere autenticación. |

Las solicitudes protegidas envían `Authorization: Bearer <access_token>`. El token de acceso dura una hora y el de renovación siete días. La renovación rota el refresh e invalida el anterior. El interceptor de Axios agrega el token y trata de renovarlo ante una respuesta 401. El login tiene un límite configurado de 30 solicitudes por minuto.

Los clientes pertenecen al grupo `clientes` y los veterinarios a `veterinarios`. En los permisos del backend, un administrador se identifica mediante `is_staff=True`. El registro público crea un usuario, lo incorpora al grupo `clientes` y crea su perfil. El registro de veterinarios está reservado a administradores.

`has_permission()` controla el acceso a una operación. `has_object_permission()` comprueba el permiso sobre un registro concreto. `get_queryset()` limita los registros accesibles y los resultados de los listados.

### Usuarios y perfiles

| Operación | Cliente | Veterinario | Administrador |
|---|---|---|---|
| Listar, consultar o eliminar usuarios | No | No | Sí |
| Consultar perfiles de clientes | Solo el propio | Todos | Todos |
| Editar perfiles de clientes | Solo el propio | No | Todos |
| Eliminar perfiles de clientes | No | No | Sí |
| Consultar perfiles de veterinarios | Sí | Sí | Sí |
| Crear, editar o eliminar veterinarios | No | No | Sí |

Consultar veterinarios requiere autenticación. El registro de clientes es público, incluso si quien lo solicita ya está autenticado. Eliminar un perfil de cliente no elimina su cuenta de usuario; la eliminación de cuentas se realiza mediante `/api/usuarios/{id}/`.

### Mascotas y atención

| Recurso u operación | Cliente | Veterinario y administrador |
|---|---|---|
| Consultar mascotas | Solo las propias | Todas |
| Crear mascotas | No | Sí |
| Editar o eliminar mascotas | Solo las propias | Todas |
| Consultar y reservar turnos | Solo para sus mascotas | Para cualquier mascota |
| Editar, eliminar o atender turnos | No | Sí |
| Cancelar turnos | Solo los propios | Cualquier turno |
| Consultar consultas, vacunas e internaciones | Solo de sus mascotas | Todas |
| Crear, editar o eliminar consultas, vacunas e internaciones | No | Sí |
| Gestionar recetas y evoluciones de internación | No | Sí |
| Gestionar horarios de veterinarios | No | Sí |

Especies y razas requieren autenticación para consultar y permisos de administrador para modificar. Los servicios y los datos generales de la clínica permiten consulta pública; su modificación requiere administrador. Las notificaciones se filtran por el usuario autenticado, también para administradores.

## Endpoints

Las rutas de listado también reciben `POST` cuando el recurso permite creación. Las rutas `/{id}/` permiten consulta y, según los permisos del recurso, `PUT`, `PATCH` y `DELETE`. `/api/usuarios/` permite únicamente listado, consulta individual y eliminación.

| Recurso | Ruta |
|---|---|
| Usuarios | `/api/usuarios/` |
| Perfiles de clientes y registro | `/api/clientes/` |
| Veterinarios | `/api/veterinarios/` |
| Horarios de veterinarios | `/api/horarios/` |
| Especies | `/api/especies/` |
| Razas | `/api/razas/` |
| Mascotas | `/api/mascotas/` |
| Servicios | `/api/servicios/` |
| Turnos | `/api/turnos/` |
| Consultas clínicas | `/api/consultas/` |
| Ítems de recetas | `/api/recetas/` |
| Vacunas | `/api/vacunas/` |
| Internaciones | `/api/internaciones/` |
| Evoluciones de internación | `/api/evoluciones-internacion/` |
| Notificaciones | `/api/notificaciones/` |
| Datos de la clínica | `/api/veterinaria/` |

Acciones de turnos:

- `POST /api/turnos/{id}/cancelar/`: cancela el turno respetando los permisos por propietario y rol.
- `POST /api/turnos/{id}/atender/`: marca el turno como atendido; solo veterinarios y administradores.

Filtros disponibles:

- Razas: `especie_id`.
- Mascotas: `usuario_id` y `solo_activas` (por defecto `true`).
- Turnos: `estado`, `mascota_id`, `veterinario_id` y `usuario_id`.
- Consultas y vacunas: `mascota`.
- Internaciones: `estado`.
- Evoluciones: `internacion`.
- Notificaciones: `leida=true` o `leida=false`.

## Validaciones

### Turnos

Las comprobaciones de reserva se realizan en `TurnoCreateSerializer.validate()`:

- Al crear un turno o cambiar su fecha, la fecha y hora deben ser posteriores al momento actual. Error: `La fecha y hora del turno deben ser futuras.`
- Para turnos sin urgencia, un horario activo del veterinario debe cubrir el día y la duración completa del servicio. Se usa la hora local de la clínica y se rechazan turnos que terminan en otro día. Error: `El veterinario no atiende en ese día y horario.`
- Se comprueban conflictos con turnos no urgentes del mismo veterinario y se excluye el propio turno al editar. La búsqueda actual usa la duración del servicio solicitado y no filtra por estado. Error: `El veterinario tiene otro turno que se solapa con este horario.`
- Las urgencias omiten las comprobaciones de horario y solapamiento, pero deben cumplir la regla de fecha futura al crearse o cambiar de fecha.
- Al editar sin cambiar fecha, veterinario ni servicio, no se repiten las comprobaciones de horario y solapamiento. Esto permite actualizar el estado de un turno pasado.

El backend verifica además que un cliente reserve únicamente para mascotas propias y marca esos turnos con `creado_por_cliente=True`. La acción de atender cambia el estado directamente, sin volver a validar la reserva.

### Otros recursos

- Los horarios de un veterinario no pueden solaparse en el mismo día.
- Al crear o editar una mascota, su dueño debe pertenecer al grupo `clientes`. La edad se calcula desde la fecha de nacimiento.
- Los datos de la clínica se limitan a un único registro.
- Al marcar una notificación como leída se registra la fecha de lectura; al desmarcarla se limpia esa fecha.

## Comandos de mantenimiento

Comprobar la configuración de Django:

```bash
docker compose --env-file .env --env-file .env.user exec backendveterinaria python manage.py check
```

Ver el estado de los servicios:

```bash
docker compose --env-file .env --env-file .env.user ps
```

Consultar los logs:

```bash
docker compose --env-file .env --env-file .env.user logs --tail=50 backendveterinaria frontend
```

Detener el proyecto conservando el volumen de PostgreSQL:

```bash
docker compose --env-file .env --env-file .env.user down
```

Para trabajar con el frontend fuera de Docker, ejecutar `npm install` y `npm run dev` desde `frontend/`, con el backend disponible en la dirección de `frontend/.env`. `npm run lint` aplica correcciones de los linters y `npm run format` formatea el código.
