from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doctor/', include('doctor.urls')),
    path('api/paciente/', include('paciente.urls')),
    path('api/resultado/', include('resultado.urls')),
    path('api/examen/', include('examen.urls')),
    path('api/solicitud/', include('solicitud.urls')),
]
