from django.urls import path
from .views import ResultadoListCreateView

urlpatterns = [
    path('', ResultadoListCreateView.as_view()),
]
