from django.urls import path
from .views import SolicitudListCreateView

urlpatterns = [
    path('', SolicitudListCreateView.as_view()),
]
