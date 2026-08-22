1. 
Bug en MascotaCreateSerializer — filtra por grupo 'Cliente' pero el grupo real se llama 'clientes'. Nadie puede crear mascotas.
2. 
URL incorrecta en veterinariaService.ts — llama a /clinica/ en vez de /veterinaria/. Los datos de la clínica dan 404.
3. 
3 interfaces del frontend usan camelCase (ConsultaClinica, Veterinaria, Notificacion) pero el backend envía snake_case. Esas vistas están rotas silenciosamente.
4. 
Cero tests — los 8 archivos tests.py están vacíos. Sin cobertura.
Altos
5. 
Sin paginación en ningún endpoint de la API. Todos los list devuelven TODO.
6. 
SECRET_KEY hardcodeada en settings.py (debería venir de .env).
7. 
Servicio Docker del backend sin healthcheck ni restart policy. Si crashea, se queda muerto.
8. 
Corre con runserver (servidor de desarrollo), no con gunicorn.
9. 
Sin rate limiting/throttling — el endpoint /api/token/ es vulnerable a fuerza bruta.
Medios
10. 
Guard de rutas del frontend no valida roles — un cliente puede navegar manualmente a /admin/dashboard.
11. 
TurnoSerializer no incluye el campo urgencia que sí existe en el modelo.
12. 
MascotaCreateSerializer no incluye observaciones.
13. 
mascotaStore y recetaStore se tragan errores sin relanzarlos. Los componentes no saben si algo falló.
14. 
Sin django-filter ni SearchFilter/OrderingFilter en los ViewSets — todo el filtrado es manual.
15. 
Sin endpoint de logout para blacklistear tokens (aunque token_blacklist está instalado).
16. 
Sin endpoint de cancelar turno (el permiso CanCancelTurno existe pero no se usa).
17. 
Sin recuperación de contraseña — solo un alert() en el frontend.
18. 
Sin vista de registro en el frontend (el backend y el store sí lo soportan).
19. 
PerfilUsuario y VeterinarioPerfil no heredan de BaseModel — inconsistencia con el resto de modelos (no tienen activo).
20. 
Formateo inconsistente de veterinario_nombre — unos usan "Apellido, Nombre", otros "Nombre Apellido".
Bajos
21. 
Directorio utils/ vacío, core/views.py es un stub muerto.
22. 
Archivos .txt basura en frontend/ y 90 líneas comentadas duplicadas en authStore.ts.
23. 
requirements.txt sin versiones pineadas. Sin .dockerignore.
24. 
Sin LOGGING configurado en Django.
25. 
Sin API versioning (/api/ en vez de /api/v1/).
26. 
Sin límites de tamaño de upload para archivos (fotos, logo).
27. 
Root package.json huérfano (echarts debería estar solo en frontend/package.json).


Funcionalidad faltante (lo más importante)
#	Qué	Por qué
1	Registro de clientes (vista)	El backend soporta POST /api/clientes/, el authStore tiene registrar(), pero no hay vista /registro. Un cliente nuevo no puede crearse una cuenta solo.
2	Recuperar contraseña	Solo un alert() en LoginView. Sin endpoint ni flujo real.
3	Cancelar turno	El permiso CanCancelTurno existe en el backend pero no hay endpoint ni botón en el frontend.
4	Logout real	cerrarSesion() solo borra variables locales. El backend tiene token blacklist instalado pero sin endpoint de logout que invalide el token.
5	El cliente no ve sus consultas/historia	Solo tiene MascotaDetalle con vacunas. Falta una vista o pestaña con el historial clínico de su mascota.
Seguridad
#	Qué	Por qué
6	Rate limiting en /api/token/	Sin throttling, el login es vulnerable a fuerza bruta.
7	SECRET_KEY hardcodeada en settings.py	Debe venir de .env. Así como está cualquiera que vea el repo puede firmar tokens JWT.
8	Validación de rol en el router del frontend	El guard solo verifica requiereAuth, no compara to.meta.roles con auth.grupo. La API igual bloquea, pero la UI se renderiza para cualquiera.
9	Sin límite de tamaño de upload	Los campos de foto/logo no tienen DATA_UPLOAD_MAX_MEMORY_SIZE.
Calidad de código
#	Qué	Por qué
10	Cero tests	8 archivos tests.py vacíos. Sin tests no podés refactorizar con confianza.
11	Paginación	Ningún endpoint pagina. Si hay 5000 turnos, el GET devuelve todo de una.
12	Helpers duplicados	formatearFecha, insigniaEstado, emojiAvatar están copiados en 8-12 vistas cada uno. Deberían ser composables o utils compartidos.
13	Stores sin re-lanzar errores	mascotaStore, recetaStore, veterinarioStore se tragan el error — los componentes no pueden reaccionar.
14	fields = "__all__" en 4 serializers	Funciona pero es frágil: si agregás un campo al modelo, se expone automáticamente en la API.
UX/UI
#	Qué	Por qué
15	Sin skeleton loaders ni transiciones	Solo texto "Cargando...". Con Bootstrap es fácil agregar placeholders.
16	Manejo de errores genérico	Si el backend está caído, el usuario ve "Error al obtener...". Sin distinguir timeout, 500, o red caída.
Infraestructura
#	Qué	Por qué
17	Sin healthcheck en el backend (Docker)	Si Django crashea, Docker no lo sabe porque no hay healthcheck ni restart: unless-stopped.
18	requirements.txt sin versiones	django en vez de django>=4.2,<5.0. Un pip install futuro puede romper todo.
19	Sin .dockerignore	Aunque ahora el .gitignore lo filtra, la build manda contexto de más.