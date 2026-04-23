from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

# ── BÁSICOS ──────────────────────────────────────────────────────────────────
router.register(r"veterinaria", views.VeterinariaViewSet)
router.register(r"especies", views.EspecieViewSet)

router.register(r"razas", views.RazaViewSet, basename="raza")
router.register(r"servicios", views.ServicioViewSet)
router.register(r"veterinarios", views.VeterinarioPerfilViewSet)
router.register(r"horarios", views.HorarioVeterinarioViewSet)
router.register(r"recetas", views.RecetaItemViewSet)

# ── CON LÓGICA EXTRA ──────────────────────────────────────────────────────────
router.register(r"usuarios", views.RegistroUsuarioViewSet)
router.register(r"perfiles", views.PerfilUsuarioViewSet)
router.register(r"mascotas", views.MascotaViewSet, basename="mascota")
router.register(r"turnos", views.TurnoViewSet, basename="turno")
router.register(r"consultas", views.ConsultaClinicaViewSet, basename="consulta")
router.register(r"vacunas", views.VacunaViewSet, basename="vacuna")
router.register(r"internaciones", views.InternacionViewSet, basename="internacion")
router.register(r"evoluciones", views.EvolucionInternacionViewSet, basename="evolucion")
router.register(r"notificaciones", views.NotificacionViewSet, basename="notificacion")


urlpatterns = [
    path("", include(router.urls)),
]
