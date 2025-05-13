from django.urls import path
from .views import ResultadoListView, ResultadoCreateView

urlpatterns = [
    path('', ResultadoListView.as_view()),
    path('', ResultadoCreateView.as_view()),
]
