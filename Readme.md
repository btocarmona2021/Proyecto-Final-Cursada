# 🐾 Sistema de Gestión Veterinaria

Sistema web completo para la gestión de una clínica veterinaria, desarrollado con **Django REST Framework** en el backend y preparado para conectarse con un frontend en **Vue.js**.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.12 | Lenguaje base |
| Django | 5.x | Framework web |
| Django REST Framework | 3.x | API REST |
| PostgreSQL | 15 | Base de datos |
| Docker | Latest | Contenedorización |
| Docker Compose | Latest | Orquestación de servicios |
| Simple JWT | Latest | Autenticación JWT |

---

## 📁 Estructura del proyecto

```
Proyecto_Final_Cursada/
├── backend/
│   ├── core/                   # App principal con modelos, serializers y vistas
│   │   ├── models.py           # Todos los modelos del sistema
│   │   ├── serializers.py      # Serializers con validaciones
│   │   ├── views.py            # ViewSets de la API
│   │   └── urls.py             # Rutas de la app
│   ├── veterinaria/            # Configuración del proyecto
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🗄️ Modelos del sistema

| Modelo | Descripción |
|---|---|
| `Veterinaria` | Datos del negocio (singleton) |
| `PerfilUsuario` | Perfil extendido de clientes |
| `VeterinarioPerfil` | Perfil extendido de veterinarios |
| `HorarioVeterinario` | Disponibilidad horaria por día |
| `Especie` | Catálogo de especies (perro, gato, etc.) |
| `Raza` | Razas vinculadas a especie |
| `Mascota` | Pacientes del sistema |
| `Servicio` | Servicios ofrecidos por la clínica |
| `Turno` | Gestión de turnos con validación de solapamiento |
| `ConsultaClinica` | Historial clínico de consultas |
| `RecetaItem` | Ítems de recetas vinculados a consultas |
| `Vacuna` | Registro de vacunación por mascota |
| `Internacion` | Gestión de internaciones |
| `EvolucionInternacion` | Notas de evolución durante internación |
| `Notificacion` | Sistema de notificaciones por usuario |

---

## 🔐 Autenticación

El sistema utiliza **JWT (JSON Web Tokens)** mediante `djangorestframework-simplejwt`.

```http
POST /api/token/          → Obtener access + refresh token
POST /api/token/refresh/  → Renovar access token
```

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <access_token>
```

---

## 📡 Endpoints disponibles

<!-- ### Autenticación
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/token/` | Login — obtener tokens |
| POST | `/api/token/refresh/` | Refrescar access token |
| POST | `/api/registro/` | Registro de nuevo usuario | -->

### Veterinaria
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/veterinaria/` | Datos de la clínica |
| PUT/PATCH | `/api/veterinaria/{id}/` | Actualizar datos |

### Especies y Razas
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/especies/` | Listar / crear especie |
| GET/PUT/DELETE | `/api/especies/{id}/` | Detalle / editar / eliminar |
| GET/POST | `/api/razas/` | Listar / crear raza |
| GET/PUT/DELETE | `/api/razas/{id}/` | Detalle / editar / eliminar |

### Mascotas
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/mascotas/` | Listar / crear mascota |
| GET/PUT/DELETE | `/api/mascotas/{id}/` | Detalle / editar / eliminar |

### Turnos
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/turnos/` | Listar / crear turno |
| GET/PUT/DELETE | `/api/turnos/{id}/` | Detalle / editar / eliminar |

### Consultas Clínicas
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/consultas/` | Listar / crear consulta |
| GET/PUT/DELETE | `/api/consultas/{id}/` | Detalle / editar / eliminar |

### Recetas
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/recetas/` | Listar / crear receta |
| GET/PUT/DELETE | `/api/recetas/{id}/` | Detalle / editar / eliminar |

### Vacunas
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/vacunas/` | Listar / crear vacuna |
| GET/PUT/DELETE | `/api/vacunas/{id}/` | Detalle / editar / eliminar |

### Internaciones
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/internaciones/` | Listar / crear internación |
| GET/PUT/DELETE | `/api/internaciones/{id}/` | Detalle / editar / eliminar |

### Evoluciones de Internación
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/evoluciones/` | Listar / crear evolución |
| GET/PUT/DELETE | `/api/evoluciones/{id}/` | Detalle / editar / eliminar |

### Notificaciones
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/notificaciones/` | Listar / crear notificación |
| GET/PUT/DELETE | `/api/notificaciones/{id}/` | Detalle / editar / eliminar |

---

## 🚀 Cómo levantar el proyecto

### Requisitos previos
- Docker
- Docker Compose

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Proyecto_Final_Cursada
```

### 2. Configurar variables de entorno

El proyecto usa dos archivos de entorno separados:

- `.env` → variables de la aplicación (base de datos, secret key, etc.)
- `.env.user` → variables del sistema del usuario (UID y GID) — **se genera automáticamente**

Crear el archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
DB_NAME=veterinaria_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### 3. Generar `.env.user` con el script

El archivo `.env.user` se genera automáticamente ejecutando el script incluido:

```bash
bash setup.sh
```

Esto crea el archivo `.env.user` con el UID y GID del usuario actual del sistema, necesario para evitar problemas de permisos en Docker.

### 4. Levantar los contenedores

```bash
docker compose --env-file .env --env-file .env.user up --build
```

### 5. Aplicar migraciones

```bash
docker compose exec backendproyecto python manage.py migrate
```

### 6. Crear superusuario

```bash
docker compose exec backendproyecto python manage.py createsuperuser
```

### 6. Acceder al sistema

| Servicio | URL |
|---|---|
| API REST | http://localhost:8000/api/ |
| Panel de administración | http://localhost:8000/admin/ |

---

## 🧪 Testing con Postman

El proyecto incluye una colección de Postman con todos los endpoints documentados y con ejemplos de JSON para cada operación (GET, POST, PUT, DELETE).

**Variable de entorno en Postman:**
```
veterinaria = http://localhost:8000
```

---

## 📌 Validaciones implementadas

- **Turnos**: No permite solapamiento de horarios para el mismo veterinario
- **Turnos**: Valida que el turno esté dentro del horario disponible del veterinario
- **Horarios**: No permite que un veterinario tenga horarios superpuestos en el mismo día
- **Veterinaria**: Solo permite registrar una única veterinaria (singleton)
- **Mascota**: El campo `microchip` es único por mascota

---

## 👨‍💻 Autor

**Alberto** — Proyecto Final de Cursada  
Año: 2026