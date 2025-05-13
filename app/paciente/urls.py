from django.urls import path
from .views import PacienteListCreateView, PacientesPorDoctorView

urlpatterns = [
    path('', PacienteListCreateView.as_view()),
    path('doctor/', PacientesPorDoctorView.as_view()),
]
