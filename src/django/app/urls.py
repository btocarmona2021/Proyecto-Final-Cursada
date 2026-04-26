from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from veterinaria.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", LoginView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/", include("veterinaria.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
