from django.urls import path
from .views import PacienteListCreateView

urlpatterns = [
    path('', PacienteListCreateView.as_view()),
]
