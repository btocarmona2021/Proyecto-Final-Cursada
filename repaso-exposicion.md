# REPASO COMPLETO — SISTEMA DE GESTIÓN VETERINARIA

## Índice

1. [Arquitectura general](#1-arquitectura-general)
2. [Un endpoint completo: GET /api/mascotas/](#2-un-endpoint-completo-get-apimascotas)
3. [JWT Custom — Cómo funciona el login](#3-jwt-custom--cómo-funciona-el-login)
4. [Clases de permisos — Quién puede hacer qué](#4-clases-de-permisos--quién-puede-hacer-qué)
5. [Reserva de turno — Punto a punto](#5-reserva-de-turno--punto-a-punto)
6. [BaseModel y Soft-Delete](#6-basemodel-y-soft-delete)
7. [Filtros por Query Params](#7-filtros-por-query-params)
8. [Registro de cliente](#8-registro-de-cliente)
9. [Interceptor de Axios](#9-interceptor-de-axios)
10. [Notificaciones](#10-notificaciones)

---

# 1. ARQUITECTURA GENERAL

```
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3 + TypeScript)         │
│  localhost:5173                                          │
│                                                          │
│  Router ───> Guards (redirige según rol)                 │
│    │                                                     │
│    ├── LoginView (pública)                               │
│    ├── AdminLayout (veterinarios + administradores)      │
│    │     └── 13 vistas (agenda, pacientes, etc.)         │
│    └── ClienteLayout (clientes)                          │
│          └── 6 vistas (inicio, mascotas, turnos, etc.)   │
│                                                          │
│  Pinia Stores (17) ───> Services ───> Axios (api.ts)     │
│                                              │            │
└──────────────────────────────────────────────┼────────────┘
                                               │ HTTP
┌──────────────────────────────────────────────┼────────────┐
│                    BACKEND (Django DRF)       │           │
│  Docker: puerto 8000                         │           │
│                                               ▼           │
│  JWT Auth (SimpleJWT)                          │           │
│  POST /api/token/ ───> { access, refresh, grupo }        │
│  POST /api/token/refresh/ ───> { access, refresh }       │
│                                                          │
│  7 apps:                                                │
│  ├── usuarios: User + Perfiles + Horarios               │
│  ├── mascotas: Especie → Raza → Mascota                  │
│  ├── agenda: Servicio + Turno                            │
│  ├── historia_clinica: Consulta → Receta + Vacuna        │
│  ├── internaciones: Internacion → Evolucion              │
│  ├── clinica: Veterinaria (singleton)                    │
│  └── notificaciones: Notificacion por usuario            │
└──────────────────────────────────────────────────────────┘
```

### Stack tecnológico

| Componente | Tecnología |
|-----------|-----------|
| Backend | Django 5 + Django REST Framework |
| Frontend | Vue 3.5 + TypeScript 6 + Pinia 3 + Vue Router 5 |
| HTTP | Axios con interceptores JWT |
| UI | Bootstrap 5 + SweetAlert2 + ECharts |
| Auth | SimpleJWT (access + refresh tokens) |
| BD | PostgreSQL 15 (Docker) |
| Infra | Docker Compose |

### Las 7 apps del backend

| App | Modelo principal | Función |
|-----|-----------------|---------|
| **usuarios** | User + PerfilUsuario + VeterinarioPerfil + HorarioVeterinario | Login JWT, perfiles, horarios |
| **mascotas** | Especie → Raza → Mascota | ABM de especies, razas y pacientes |
| **agenda** | Servicio + Turno | Gestión de servicios y turnos |
| **historia_clinica** | ConsultaClinica → RecetaItem, Vacuna | Historial médico |
| **internaciones** | Internacion → EvolucionInternacion | Hospitalizaciones |
| **clinica** | Veterinaria (singleton) | Datos de la clínica |
| **notificaciones** | Notificacion | Notificaciones por usuario |
| **core** | BaseModel + todas las clases de permisos | Base abstracta + seguridad |

---

# 2. UN ENDPOINT COMPLETO: GET /api/mascotas/

## El recorrido paso a paso

Imaginate que el sistema es un negocio con una recepcionista.

**Vos (cliente)** llegás y le pedís: *"Dame la lista de mis mascotas"*

**La recepcionista** hace 4 cosas en orden:

### Paso 1 — Preguntar quién sos (Permission)

> *"A ver... ¿estás logueado? ¿tenés token?"*
- Si no tenés token → te echa (401)
- Si tenés token → te deja pasar

### Paso 2 — Buscar SOLO tus datos (get_queryset)

> *"Sos el cliente Juan. Voy a buscar en el archivero SOLO las mascotas donde diga 'dueño: Juan'. Las de otros dueños ni las toco."*

Acá es donde tu vecino **nunca ve a Firulais** y vos **nunca ves a Mishi**.

### Paso 3 — Ponerle formato (Serializer)

> *"Bueno, en el archivero dice 'sexo: M'. Pero en vez de mandarte una M, te pongo 'Macho' que se entiende mejor. Y en vez de mandar la fecha de nacimiento sola, te calculo la edad en años."*

### Paso 4 — Entregarte el papel (Response)

> *"Tomá, Juan. Estas son tus mascotas: Firulais (Labrador, 3 años) y Rocky (Caniche, 1 año)."*

## El código real

### 1. URL (`mascotas/urls.py`)
```python
router.register(r'mascotas', MascotaViewSet)
```
DRF convierte eso automáticamente en:
- `GET /api/mascotas/` → list()
- `GET /api/mascotas/5/` → retrieve(5)
- `POST /api/mascotas/` → create()
- `PUT /api/mascotas/5/` → update()
- `DELETE /api/mascotas/5/` → destroy()

### 2. ViewSet (`mascotas/views.py`)
```python
class MascotaViewSet(ModelViewSet):
    queryset = Mascota.objects.select_related('raza', 'raza__especie', 'usuario')
    permission_classes = [IsAuthenticated, CanManageMascota]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MascotaCreateSerializer
        return MascotaSerializer
```

### 3. get_queryset() — la seguridad real
```python
def get_queryset(self):
    queryset = super().get_queryset()
    user = self.request.user

    # SEGURIDAD: Si es cliente, solo ve SUS mascotas
    if user.groups.filter(name="clientes").exists():
        queryset = queryset.filter(usuario=user)

    # Filtros opcionales
    usuario_id = self.request.query_params.get('usuario_id')
    if usuario_id:
        queryset = queryset.filter(usuario_id=usuario_id)

    solo_activas = self.request.query_params.get('solo_activas', 'true')
    if solo_activas.lower() == 'true':
        queryset = queryset.filter(activo=True)

    return queryset
```

**Traducción a SQL:**

Si el usuario es cliente (id=5):
```sql
SELECT * FROM mascota_mascota
WHERE usuario_id = 5
  AND activo = TRUE;
```

Si el usuario es vet/admin:
```sql
SELECT * FROM mascota_mascota
WHERE activo = TRUE;
```

### 4. Permission (`core/permissions.py`)
```python
class CanManageMascota(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:   # GET
            return True                       # todos pasan
        if request.method == 'POST':          # crear
            return is_staff_or_vet(user)      # solo vet/admin
        return True  # PUT/PATCH/DELETE → deja pasar, se valida en has_object_permission

    def has_object_permission(self, request, view, obj):
        if is_staff_or_vet(user):             # vet/admin puede todo
            return True
        return obj.usuario == user            # cliente solo si es su mascota
```

### 5. Serializer (`mascotas/serializers.py`)
```python
class MascotaSerializer(ModelSerializer):
    raza_nombre = serializers.CharField(source='raza.nombre')
    especie_nombre = serializers.CharField(source='raza.especie.nombre')
    edad_anos = serializers.SerializerMethodField()
    sexo_display = serializers.CharField(source='get_sexo_display')
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'raza_nombre', 'especie_nombre',
                  'fecha_nacimiento', 'edad_anos', 'sexo_display',
                  'peso_actual', 'usuario_nombre', ...]
```

### 6. Lo que devuelve (JSON)
```json
[
  {
    "id": 1,
    "nombre": "Firulais",
    "raza_nombre": "Labrador",
    "especie_nombre": "Perro",
    "edad_anos": 3,
    "sexo_display": "Macho",
    "peso_actual": "28.50",
    "usuario_nombre": "Juan Pérez",
    "activo": true
  }
]
```

## Resumen

> **get_queryset** busca solo lo tuyo, **permission** te deja entrar según quién seas, y **serializer** le da formato bonito.

---

# 3. JWT CUSTOM — CÓMO FUNCIONA EL LOGIN

## Los dos tokens

| Token | Duración | ¿Para qué sirve? |
|-------|----------|-----------------|
| **access** | 1 hora | Identificación rápida. Se manda en cada request |
| **refresh** | 7 días | Renovador. Cuando expira el access, con este pedís uno nuevo sin volver a loguearte |

## El login paso a paso

### 1. Mandás usuario y contraseña
```
POST /api/token/
{ "username": "juan", "password": "secreto123" }
```

### 2. Django verifica credenciales

### 3. El código custom (`usuarios/token_personalizado.py`) agrega datos extra
```python
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username       # va dentro del JWT
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id           # va en la respuesta
        data['username'] = self.user.username
        data['email'] = self.user.email
        first_group = self.user.groups.first()
        data['grupo'] = first_group.name if first_group else None  # ⬅️ clave
        return data
```

### 4. Respuesta que recibe el frontend
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": 15,
  "username": "juan",
  "email": "juan@gmail.com",
  "grupo": "clientes"
}
```

Ese `grupo` es lo que el frontend usa para saber si te manda al panel de cliente, admin, o veterinario.

## ¿Por qué es "custom"?

SimpleJWT por defecto solo devuelve `access` y `refresh`. Nosotros le agregamos:
- `grupo` → el frontend sabe a dónde redirigir
- `user_id`, `username`, `email` → comodidad para no pedirlos después

## ¿Por qué dos tokens y no uno solo?

| Token único largo | Token único corto | Dos tokens |
|------------------|-------------------|------------|
| Si te lo roban, tienen acceso por días | Usuario se desloguea a cada rato | Access dura 1h (seguro), refresh dura 7d (cómodo) |

## El refresh automático
Cuando el access expira (1 hora), el frontend automáticamente manda:
```
POST /api/token/refresh/
{ "refresh": "el refresh token" }
```
Y el backend devuelve:
```json
{ "access": "nuevo token", "refresh": "nuevo refresh (el viejo se invalida)" }
```
Con `ROTATE_REFRESH_TOKENS=True` y `BLACKLIST_AFTER_ROTATION=True`, cada refresh invalida el anterior. Si alguien roba un refresh viejo, no sirve.

## Configuración en settings.py
```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

---

# 4. CLASES DE PERMISOS — QUIÉN PUEDE HACER QUÉ

## Los 3 roles (grupos)

| Grupo | ¿Quién lo tiene? | Creado por |
|-------|-----------------|-----------|
| `clientes` | Dueños de mascotas | Se registran solos (`POST /api/clientes/` público) |
| `veterinarios` | Staff médico | Solo admin |
| `administradores` | Superusuarios Django | Django admin |

## Todas las clases de permisos

### Simples (solo chequean grupo)
| Clase | ¿Qué permite? |
|-------|--------------|
| `IsAuthenticated` | Cualquiera logueado |
| `IsAdminUser` | Solo staff Django |
| `IsCliente` | Solo grupo `clientes` |
| `IsVeterinario` | Solo grupo `veterinarios` |
| `IsVeterinarioOrAdmin` | Vet o admin |
| `ReadOnly` | Solo GET/HEAD/OPTIONS (sin auth) |

### Específicas (con lógica por método)
| Clase | GET | POST | PUT/PATCH/DELETE |
|-------|-----|------|-----------------|
| `CanManageMascota` | Todos | Solo vet/admin | Dueño o staff |
| `CanManageTurno` | Todos | Todos | Solo vet/admin |
| `CanManageEspecieRaza` | Todos | Solo admin | Solo admin |
| `CanManageServicio` | Todos | Solo admin | Solo admin |
| `CanManageVeterinarioPerfil` | Todos | Solo admin | Solo admin |

### Genéricas (reutilizables)
| Clase | ¿Qué hace? |
|-------|-----------|
| `IsOwnerOrReadOnly` | GET todos, modificar solo dueño del objeto (tiene campo `usuario`) |
| `IsOwnerOrStaff` | Dueño o staff pueden todo |

## Cómo se escribe un permiso (ejemplo `CanManageMascota`)

```python
class CanManageMascota(BasePermission):
    # NIVEL 1: ¿podés entrar al endpoint?
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:      # GET → todos pasan
            return True
        if request.method == 'POST':             # POST → solo vet/admin
            return is_staff_or_vet(user)
        return True  # PUT/PATCH/DELETE → todos pasan, se valida en nivel 2

    # NIVEL 2: ¿podés tocar ESTA mascota en particular?
    def has_object_permission(self, request, view, obj):
        if is_staff_or_vet(user):              # vet/admin → todo OK
            return True
        return obj.usuario == user             # cliente → solo si es suya
```

### El flujo para DELETE

| Paso | ¿Quién pregunta? | Dueño de Firulais | Otro cliente |
|------|-----------------|-------------------|--------------|
| 1 | `has_permission` → "¿podés entrar?" | ✅ Pasa (todos pasan para DELETE) | ✅ Pasa |
| 2 | `has_object_permission` → "¿Firulais es tuyo?" | ✅ Sí | ❌ No |
| **Resultado** | | **✅ Puede borrar** | **❌ No puede** |

## Dónde se aplican (en cada ViewSet)
```python
class MascotaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CanManageMascota]
    # Se lee: "primero asegurate de que esté logueado, después chequeá si puede gestionar esta mascota"
```

## Helpers (funciones auxiliares)
```python
def is_cliente(user):      # user.groups.filter(name='clientes').exists()
def is_veterinario(user):  # user.groups.filter(name='veterinarios').exists()
def is_staff_or_vet(user): # user.is_staff or user.groups.filter(name='veterinarios').exists()
```

## Matriz de acceso completa

| Recurso | GET | POST | PUT/PATCH/DELETE |
|---------|-----|------|-----------------|
| Usuarios | Todos logueados | ❌ (read-only) | ❌ |
| Clientes | Todos | Público (registro) | Autenticado |
| Veterinarios | Todos | Solo admin | Solo admin |
| Mascotas | Todos (filtrado) | Solo vet/admin | Dueño o staff |
| Turnos | Todos (filtrado) | Todos (validado) | Solo vet/admin |
| Consultas | Todos (filtrado) | Solo vet/admin | Solo vet/admin |
| Recetas | Solo vet/admin | Solo vet/admin | Solo vet/admin |
| Vacunas | Todos (filtrado) | Solo vet/admin | Solo vet/admin |
| Internaciones | Todos (filtrado) | Solo vet/admin | Solo vet/admin |
| Evoluciones | Solo vet/admin | Solo vet/admin | Solo vet/admin |
| Especies/Razas | Todos | Solo admin | Solo admin |
| Servicios | Todos | Solo admin | Solo admin |
| Notificaciones | Solo las propias | Solo las propias | Solo las propias |

---

# 5. RESERVA DE TURNO — PUNTO A PUNTO

Escenario: Juancito (cliente) quiere reservar un turno para Firulais.

## PARTE 1 — EL FRONTEND (Vue)

### 1. Juancito entra a `/cliente/reservar`

`ReservarView.vue` carga 3 cosas al mismo tiempo:

```js
onMounted(async () => {
  await Promise.all([
    mascotaStore.obtenerTodos(),    // sus mascotas
    servicioStore.obtenerTodos(),    // servicios
    veterinarioStore.obtenerTodos(), // veterinarios
  ])
})
```

Cada store llama a su servicio → Axios con JWT → backend.

### 2. Wizard de 3 pasos

| Paso | Lo que elige | Se guarda en |
|------|-------------|-------------|
| 1 | Mascota (Firulais, id=5) | `form.mascota = 5` |
| 2 | Servicio (Control general, id=3) + motivo | `form.servicio = 3` |
| 3 | Veterinario (Dra. García, id=2) + fecha/hora | `form.veterinario = 2` |

### 3. Click "Confirmar turno"

```js
async function confirmarTurno() {
  const datos: TurnoForm = {
    fecha_hora: "2025-06-16T09:00:00",
    mascota: 5,
    veterinario: 2,
    servicio: 3,
    estado: 'reservado',
    motivo_consulta: 'Control anual',
    urgencia: false,
    creado_por_cliente: true,   // ⬅️ marca que lo creó el cliente
  }

  await turnoStore.crear(datos)
  router.push({ name: 'ClienteTurnos' })
}
```

### 4. Store → Service → HTTP
```
turnoStore.crear(datos)
  → turnosService.crear(datos)
    → POST /api/turnos/
      Header: Authorization: Bearer <JWT de Juancito>
      Body: { fecha_hora, mascota: 5, veterinario: 2, ... }
```

## PARTE 2 — EL BACKEND (Django)

### 5. `TurnoViewSet.create()`

Primero el permiso `CanManageTurno.has_permission()`:

```python
# GET y POST → todos pasan
if request.method in ['GET', 'POST']:
    return True
```

Juancito pasa.

### 6. Se elige el serializer

```python
def get_serializer_class(self):
    if self.action in ['create', 'update', 'partial_update']:
        return TurnoCreateSerializer
    return TurnoSerializer
```

### 7. `TurnoCreateSerializer.validate()` — evita cruce de horarios

```python
def validate(self, data):
    veterinario = data.get('veterinario')
    fecha_hora = data.get('fecha_hora')
    servicio = data.get('servicio')
    urgencia = data.get('urgencia', False)

    # Si es urgencia, no validar solapamiento
    if urgencia:
        return data

    duracion = timedelta(minutes=servicio.duracion_estimada)
    fecha_hora_fin = fecha_hora + duracion

    # Buscar turnos del mismo vet que se solapen
    turnos_conflicto = Turno.objects.filter(
        veterinario=veterinario,
        urgencia=False,
    ).exclude(fecha_hora__gte=fecha_hora_fin)\
     .exclude(fecha_hora__lt=fecha_hora - duracion)

    if turnos_conflicto.exists():
        raise ValidationError(
            "El veterinario tiene otro turno que se solapa con este horario."
        )

    return data
```

### 8. `perform_create()` — la seguridad real

```python
def perform_create(self, serializer):
    user = self.request.user        # Juancito
    mascota = serializer.validated_data['mascota']  # Firulais

    if user.groups.filter(name="clientes").exists():
        # ¿Firulais es de Juancito?
        if mascota.usuario != user:
            raise PermissionDenied("No puede crear turnos para mascotas ajenas.")
        serializer.save(creado_por_cliente=True)
    else:
        serializer.save()
```

Si Juancito intentara crear un turno para Mishi (de otro dueño):
- Por UI: nunca ve a Mishi en el select (el `get_queryset()` de mascotas ya filtró)
- Por API directa: `mascota.usuario != user` → error 403

**Defensa en capas.**

### 9. Se guarda en la BD
```sql
INSERT INTO agenda_turno (fecha_hora, mascota_id, veterinario_id, servicio_id,
                          estado, motivo_consulta, creado_por_cliente)
VALUES ('2025-06-16 09:00:00', 5, 2, 3, 'reservado', 'Control anual', TRUE);
```

### 10. Respuesta al frontend
```json
{
  "id": 42,
  "fecha_hora": "2025-06-16T09:00:00",
  "mascota_nombre": "Firulais",
  "veterinario_nombre": "Dra. García",
  "servicio_nombre": "Control general",
  "estado_display": "Reservado",
  "creado_por_cliente": true
}
```

## PARTE 3 — VUELTA AL FRONTEND

El store recibe el turno y lo agrega a la lista local:
```js
const nuevo = await turnosService.crear(data)
turnos.value.push(nuevo)
```

Redirige a `/cliente/turnos` y Juancito ve su turno.

## Diagrama completo

```
RESERVAR VIEW                    BACKEND
─────────────                    ───────
Paso 1: elige Firulais
Paso 2: elige Control general
Paso 3: elige Dra. García + 09:00
    │
    └─ Confirmar ──POST /api/turnos/──→ TurnoViewSet
                                           │
                              ┌────────────┼────────────┐
                              │            │            │
                         CanManage   validate()  perform_create()
                         Turno       (cruce     (¿Firulais
                         (permiso)    horario?)   es suyo?)
                              │            │            │
                              ✅            ✅          ✅
                              │            │            │
                              └────────────┼────────────┘
                                           │
                                    INSERT INTO agenda_turno
                                    (creado_por_cliente = TRUE)
                                           │
                    ←─── 201 Created ──────┘
    │
    └─ Redirige a /cliente/turnos ✅
```

## Las 3 capas de seguridad en un POST de turno

| Capa | ¿Qué chequea? | Código |
|------|-------------|--------|
| `CanManageTurno` | ¿Puede entrar? | POST → todos pasan |
| `validate()` | ¿El vet está libre? | Cruce de horarios |
| `perform_create()` | ¿La mascota es suya? | `mascota.usuario != user` |

---

# 6. BASEMODEL Y SOFT-DELETE

## El problema

Si borrás una mascota con `DELETE` de verdad, desaparece de la base de datos. Con ella se van todos sus turnos, consultas, vacunas (por el `CASCADE`).

En un sistema real eso es peligroso. Ejemplo: dueño se enoja, pide borrar su mascota, y perdés todo el historial médico.

## La solución: no borrar, desactivar

```python
# core/models.py
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)    # ⬅️ el truco

    class Meta:
        abstract = True  # no crea tabla, solo se hereda
```

Casi todos los modelos heredan de `BaseModel`:
```python
class Mascota(BaseModel):   # tiene created_at, updated_at, activo
    nombre = ...
    raza = ...
```

## Cómo se usa

Los ViewSets filtran por `activo=True` por defecto:
```python
# EspecieViewSet, RazaViewSet, ServicioViewSet
queryset = MiModelo.objects.filter(activo=True)

# MascotaViewSet (con opción de ver inactivas)
solo_activas = self.request.query_params.get('solo_activas', 'true')
if solo_activas.lower() == 'true':
    queryset = queryset.filter(activo=True)
```

"Borrar" sería en realidad:
```python
mascota.activo = False
mascota.save()
```

## DELETE real vs Soft-Delete

| DELETE real | Soft-delete |
|------------|-------------|
| Datos perdidos para siempre | Datos ocultos pero recuperables |
| Rompe relaciones (CASCADE) | Relaciones intactas |
| No hay auditoría | Sabés cuándo se desactivó (`updated_at`) |
| No se puede deshacer | Se puede reactivar con `activo = True` |

> **Nota:** El proyecto tiene el campo `activo` en los modelos que heredan de `BaseModel`, y los ViewSets filtran por él. Pero el `destroy()` de los ViewSets todavía hace DELETE real en la DB. En una versión futura se puede cambiar para que haga `activo = False` en vez de borrar.

## Modelos que NO heredan de BaseModel

- `User` (de Django)
- `PerfilUsuario`
- `VeterinarioPerfil`

Estos no tienen campo `activo` porque no aplica (no se "desactiva" un usuario, se desactiva la cuenta).

---

# 7. FILTROS POR QUERY PARAMS

## ¿Qué son?

Son los parámetros que van en la URL después del `?`. Permiten traer solo los datos que necesitás en vez de todo.

```
/api/turnos/?estado=reservado&mascota_id=5
              └──┬──┘     └─────┬────┘
          filtro 1          filtro 2
```

## Cómo se obtienen en Django

```python
self.request.query_params.get('nombre_del_parametro')
```

`query_params` es un diccionario con todo lo que viene después del `?`. Si el parámetro no viene, devuelve `None`.

## Ejemplo 1 — Turnos por estado

```
GET /api/turnos/?estado=reservado
```

```python
# agenda/views.py
estado = self.request.query_params.get("estado")    # "reservado"

if estado:
    queryset = queryset.filter(estado=estado)       # WHERE estado = 'reservado'
```

Traducción SQL:
```sql
SELECT * FROM agenda_turno WHERE estado = 'reservado';
```

## Ejemplo 2 — Turnos de una mascota

```
GET /api/turnos/?mascota_id=5
```

```python
mascota_id = self.request.query_params.get("mascota_id")

if mascota_id:
    queryset = queryset.filter(mascota_id=mascota_id)
```

## Ejemplo 3 — Razas de una especie

```
GET /api/razas/?especie_id=2
```

```python
especie_id = self.request.query_params.get('especie_id')

if especie_id:
    queryset = queryset.filter(especie_id=especie_id)
```

Si especie 2 es "Felino", devuelve solo razas de gatos.

## Ejemplo 4 — Valor por defecto

```
GET /api/mascotas/              → solo activas
GET /api/mascotas/?solo_activas=false  → todas (activas e inactivas)
```

```python
solo_activas = self.request.query_params.get('solo_activas', 'true')
#              si no viene el parámetro ────────────┘ usa 'true'

if solo_activas.lower() == 'true':
    queryset = queryset.filter(activo=True)
```

| URL | `solo_activas` | Resultado |
|-----|---------------|-----------|
| `/api/mascotas/` | no viene → `'true'` | Solo activas |
| `/api/mascotas/?solo_activas=false` | `'false'` | Todas |
| `/api/mascotas/?solo_activas=true` | `'true'` | Solo activas |

## Ejemplo 5 — Admin busca turnos de un dueño específico

```
GET /api/turnos/?usuario_id=3
```

```python
usuario_id = self.request.query_params.get("usuario_id")

if usuario_id:
    queryset = queryset.filter(mascota__usuario_id=usuario_id)
```

El `__` (doble guion bajo) es la magia de Django ORM: **sigue la relación**. `mascota__usuario_id` = "andá a la tabla mascota, de ahí fijate el campo usuario_id".

SQL generado:
```sql
WHERE mascota.usuario_id = 3
```

## Todos los filtros disponibles

| Endpoint | Filtro | Ejemplo |
|----------|--------|---------|
| `/api/turnos/` | `?estado=` | `?estado=confirmado` |
| `/api/turnos/` | `?mascota_id=` | `?mascota_id=5` |
| `/api/turnos/` | `?veterinario_id=` | `?veterinario_id=2` |
| `/api/turnos/` | `?usuario_id=` | `?usuario_id=3` |
| `/api/razas/` | `?especie_id=` | `?especie_id=2` |
| `/api/mascotas/` | `?usuario_id=` | `?usuario_id=3` |
| `/api/mascotas/` | `?solo_activas=` | `?solo_activas=false` |
| `/api/consultas/` | `?mascota=` | `?mascota=5` |
| `/api/vacunas/` | `?mascota=` | `?mascota=5` |
| `/api/internaciones/` | `?estado=` | `?estado=internado` |
| `/api/evoluciones-internacion/` | `?internacion=` | `?internacion=8` |
| `/api/notificaciones/` | `?leida=` | `?leida=true` |

## En el código completo de TurnoViewSet

```python
def get_queryset(self):
    queryset = Turno.objects.select_related("mascota", "veterinario", "servicio")

    # Seguridad: clientes solo ven sus turnos
    if user.groups.filter(name="clientes").exists():
        queryset = queryset.filter(mascota__usuario=user)

    # Filtros opcionales
    estado = self.request.query_params.get("estado")
    mascota_id = self.request.query_params.get("mascota_id")
    veterinario_id = self.request.query_params.get("veterinario_id")
    usuario_id = self.request.query_params.get("usuario_id")

    if estado:            queryset = queryset.filter(estado=estado)
    if mascota_id:        queryset = queryset.filter(mascota_id=mascota_id)
    if veterinario_id:    queryset = queryset.filter(veterinario_id=veterinario_id)
    if usuario_id:        queryset = queryset.filter(mascota__usuario_id=usuario_id)

    return queryset
```

## Resumen

> **query_params** = lo que viene en la URL después del `?`. Cada ViewSet decide si filtra o no según lo que recibe. Si el parámetro no viene, no filtra por ese campo.

---

# 8. REGISTRO DE CLIENTE

## El flujo público

El registro del cliente es **el único endpoint público del sistema** (no necesita JWT). Cualquier persona puede crear una cuenta.

```
POST /api/clientes/
{ "username": "juanperez", "password": "secreto123", "first_name": "Juan",
  "last_name": "Pérez", "email": "juan@gmail.com", "telefono": "123456789" }
```

## El serializer que lo maneja

```python
# usuarios/serializers.py
class ClienteRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    direccion = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name",
                  "last_name", "email", "telefono", "direccion"]

    def create(self, validated_data):
        telefono = validated_data.pop('telefono', '')
        direccion = validated_data.pop('direccion', '')
        password = validated_data.pop('password')

        # 1. Crear el usuario en auth.User
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # 2. Asignar al grupo clientes
        grupo, _ = Group.objects.get_or_create(name='clientes')
        user.groups.add(grupo)

        # 3. Crear el perfil del cliente
        PerfilUsuario.objects.create(
            usuario=user,
            telefono=telefono,
            direccion=direccion
        )

        return user
```

## Lo que hace paso a paso

1. **Crea el `User`** en Django auth (username, password, nombres, email)
2. **Asigna el grupo** `clientes` automáticamente
3. **Crea el `PerfilUsuario`** con teléfono y dirección
4. Devuelve el usuario creado (sin password)

## El ViewSet

```python
# usuarios/views.py
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ClienteRegistroSerializer   # ⬅️ para POST
        return PerfilUsuarioSerializer         # para GET/PUT

    def get_permissions(self):
        if self.action == 'create':
            return []  # ⬅️ público, sin permisos
        return super().get_permissions()
```

El truco está en que `get_permissions()` devuelve una lista vacía para `create` — no necesita autenticación. Para todas las demás acciones (GET, PUT, DELETE), requiere estar logueado.

## En el frontend

```js
// authStore.ts
const registrar = async (data: RegistroClienteForm) => {
    await authService.registrar(data)
    router.push('/login')   // redirige al login para que se loguee
}
```

El flujo completo: registrarse → ir al login → loguearse → al panel del cliente.

## Diferencia con registro de veterinario

| | Cliente | Veterinario |
|--|---------|------------|
| Endpoint | `POST /api/clientes/` | `POST /api/veterinarios/` |
| ¿Público? | Sí (cualquiera se registra) | No (solo admin puede crear) |
| Grupo asignado | `clientes` | `veterinarios` |
| Perfil creado | `PerfilUsuario` | `VeterinarioPerfil` |
| Campos extra | teléfono, dirección | matrícula, especialidad |

---

# 9. INTERCEPTOR DE AXIOS

## ¿Qué es un interceptor?

Es un código que se ejecuta automáticamente en **cada request** y **cada response** HTTP. Como un guardia que revisa todos los paquetes antes de que salgan o después de que lleguen.

## El archivo completo (`frontend/src/api/api.ts`)

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})
```

## Interceptor de REQUEST (antes de enviar)

```typescript
api.interceptors.request.use(async (config) => {
  const { useAuthStore } = await import('@/stores/authStore')
  const authStore = useAuthStore()

  if (authStore.tokenAcceso) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
  }

  return config
})
```

**¿Qué hace?**

Antes de cada request a la API:
1. Importa el authStore
2. Toma el token de acceso
3. Lo inyecta en el header `Authorization: Bearer <token>`

**Ejemplo:** si Juancito hace `GET /api/mascotas/`, el request que realmente sale es:
```
GET /api/mascotas/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

El backend recibe el token, lo valida, y sabe quién es Juancito.

## Interceptor de RESPONSE (cuando llega la respuesta)

```typescript
api.interceptors.response.use(
  (response) => response,                          // si OK, no hace nada
  async (error) => {
    const original = error.config

    if (!error.response) {
      return Promise.reject(error)
    }

    // ¿Error 401 y no se ha reintentado?
    if (error.response.status === 401 && !original._reintento) {
      original._reintento = true                    // marca para no reintentar infinito

      const { useAuthStore } = await import('@/stores/authStore')
      const authStore = useAuthStore()

      if (!authStore.tokenRefresco) {                // no hay refresh → cerrar sesión
        authStore.cerrarSesion()
        return Promise.reject(error)
      }

      try {
        await authStore.refrescarToken()             // pedir nuevo access token
        original.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
        return api(original)                          // reintentar el request original
      } catch {
        authStore.cerrarSesion()                      // si falla el refresh → cerrar sesión
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  },
)
```

**¿Qué hace?**

Cuando el backend responde con error:

1. Si el error no es 401 → lo pasa sin tocar
2. Si es 401 y ya se reintentó → lo pasa sin tocar
3. Si es 401 y **no** se reintentó:
   - Toma el refresh token del store
   - Si no hay refresh → cierra sesión (redirige a login)
   - Si hay refresh → llama a `authStore.refrescarToken()`
   - El refrescarToken manda `POST /api/token/refresh/` con el refresh
   - Backend devuelve un nuevo access token
   - Se actualiza el access en store y localStorage
   - Se **reintenta el request original** con el nuevo token

## El flujo completo de refresh automático

```
1. Juancito hace GET /api/mascotas/
   → Request interceptor: mete Bearer <access_token>

2. El access token expiró (1 hora)
   → Backend responde: 401 Unauthorized

3. Response interceptor atrapa el 401
   → No se ha reintentado todavía
   → Hay refresh token? Sí
   → Llama a authStore.refrescarToken()
       → POST /api/token/refresh/ con el refresh
       → Backend devuelve nuevo access
       → Se guarda en store + localStorage

4. Se modifica el request original con el nuevo token
   → Authorization: Bearer <nuevo_access>

5. Se reenvía el GET /api/mascotas/
   → Backend responde 200 OK con las mascotas

6. Juancito ni se enteró de que el token expiró
```

## El authStore que lo respalda

```typescript
// stores/authStore.ts
const tokenAcceso = ref<string | null>(localStorage.getItem('accessToken'))
const tokenRefresco = ref<string | null>(localStorage.getItem('refreshToken'))
const grupo = ref<string | null>(localStorage.getItem('grupo'))

const iniciarSesion = async (credentials) => {
    const tokens = await authService.login(credentials)
    tokenAcceso.value = tokens.access
    tokenRefresco.value = tokens.refresh
    grupo.value = maybeWithGroup.grupo
    localStorage.setItem('accessToken', tokens.access)
    localStorage.setItem('refreshToken', tokens.refresh)
    localStorage.setItem('grupo', maybeWithGroup.grupo ?? '')
    router.push(redireccionPorGrupo())
}

const refrescarToken = async () => {
    const tokens = await authService.refreshToken(tokenRefresco.value)
    tokenAcceso.value = tokens.access
    tokenRefresco.value = tokens.refresh
    localStorage.setItem('accessToken', tokens.access)
    localStorage.setItem('refreshToken', tokens.refresh)
}

const cerrarSesion = () => {
    tokenAcceso.value = null
    tokenRefresco.value = null
    grupo.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('grupo')
    router.push('/login')
}
```

## Resumen

| Momento | ¿Qué hace? |
|---------|-----------|
| Antes de cada request | Inyecta el access token en el header |
| Cuando el token expira (401) | Renueva automáticamente con el refresh |
| Cuando no hay refresh | Cierra sesión y redirige a login |
| Todo esto | **Sin que el usuario se dé cuenta** |

---

# 10. NOTIFICACIONES

## El modelo

```python
# notificaciones/models.py
class Notificacion(BaseModel):
    class Tipo(models.TextChoices):
        TURNO = "turno", "Turno"
        VACUNA = "vacuna", "Vacuna"
        INTERNACION = "internacion", "Internación"
        SISTEMA = "sistema", "Sistema"

    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="notificaciones")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)
```

Hereda de `BaseModel`, así que también tiene `created_at`, `updated_at` y `activo`.

## El serializer

```python
# notificaciones/serializers.py
class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = "__all__"
        read_only_fields = ["id", "fecha_lectura", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        # Si se marca como leída y antes no lo estaba
        if validated_data.get('leida') and not instance.leida:
            validated_data['fecha_lectura'] = timezone.now()

        # Si se desmarca, limpiar fecha
        if not validated_data.get('leida', instance.leida):
            validated_data['fecha_lectura'] = None

        return super().update(instance, validated_data)
```

Auto-maneja la fecha de lectura: cuando marcás como leída, guarda la fecha automáticamente.

## El ViewSet

```python
# notificaciones/views.py
class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # SEGURIDAD: Cada usuario solo ve SUS notificaciones
        queryset = Notificacion.objects.select_related("usuario").filter(
            usuario=self.request.user
        )

        # Filtro opcional
        leida = self.request.query_params.get("leida")
        if leida is not None:
            queryset = queryset.filter(leida=leida.lower() == "true")

        return queryset.order_by("-created_at")
```

**Seguridad clave:** `usuario=self.request.user` — nadie puede ver notificaciones de otro usuario.

## Filtros disponibles

```
GET /api/notificaciones/            → todas las del usuario
GET /api/notificaciones/?leida=true → solo leídas
GET /api/notificaciones/?leida=false → solo no leídas
```

## En el frontend (ClienteLayout)

El `ClienteLayout.vue` tiene:

1. **Un badge en la campanita** que muestra el contador de no leídas
2. **Un panel deslizable** que se abre al clickear la campanita
3. Muestra hasta 10 notificaciones, cada una con color según tipo

### Store de notificaciones

```typescript
// stores/notificacionStore.ts
const notificaciones = ref<Notificacion[]>([])
const noLeidas = computed(() => notificaciones.value.filter(n => !n.leida).length)
```

### En el layout

```vue
<button @click="abrirPanelNotificaciones">
  🔔 {{ notificacionStore.noLeidas }}
</button>

<PanelNotificaciones v-if="panelAbierto" :notificaciones="notificaciones" />
```

## Tipos de notificaciones y su color

| Tipo | Color | Ejemplo |
|------|-------|---------|
| `turno` | Azul | "Tu turno con Firulais es mañana a las 09:00" |
| `vacuna` | Verde | "Recordatorio: vacuna antirrábica vence en 15 días" |
| `internacion` | Rojo | "Firulais está internado en observación" |
| `sistema` | Gris | "Bienvenido a VetSystem" |

## Resumen

> Las notificaciones son el único recurso donde el filtro de seguridad es **siempre** `usuario=self.request.user`. No hay opción de ver notificaciones ajenas, ni siquiera como admin.
