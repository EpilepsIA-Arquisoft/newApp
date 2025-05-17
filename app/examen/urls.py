from django.urls import path
from .views import ResultadoExamenCreateView, ExamenCreateView, ExamenListView, ResultadoExamenDetailView

urlpatterns = [
    path('', ExamenListView.as_view()),
    path('upload/', ExamenCreateView.as_view()),
    path('<str:examen_id>/resultado/', ResultadoExamenDetailView.as_view()),
    path('<str:examen_id>/resultado/upload/', ResultadoExamenCreateView.as_view()),
]
