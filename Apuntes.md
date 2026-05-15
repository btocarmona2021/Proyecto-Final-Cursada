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