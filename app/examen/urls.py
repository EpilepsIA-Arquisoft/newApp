from django.urls import path
from .views import ResultadoExamenCreateView, ExamenCreateView, ExamenListView, ResultadoExamenDetailView

urlpatterns = [
    path('', ExamenCreateView.as_view()),
    path('', ExamenListView.as_view()),
    path('<int:examen_id>/resultado/', ResultadoExamenCreateView.as_view()),
    path('<int:examen_id>/resultado/', ResultadoExamenDetailView.as_view()),

]
