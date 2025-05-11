from django.urls import path
from .views import CrearResultadoExamenView, ExamenListCreateView

urlpatterns = [
    path('', ExamenListCreateView.as_view()),
    path('<int:examen_id>/resultado/', CrearResultadoExamenView.as_view()),  # Endpoint para crear el resultado de un examen

]
