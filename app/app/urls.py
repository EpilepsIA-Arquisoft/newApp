from django.contrib import admin
from django.urls import path, include

from .views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    #path('doctor/', include('doctor.urls')),
    path('paciente/', include('paciente.urls')),
    #path('resultado/', include('resultado.urls')),
    path('examen/', include('examen.urls')),
    path('solicitud/', include('solicitud.urls')),
    path('health', health_check, name='health'),
]
