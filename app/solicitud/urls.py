from django.urls import path
from .views import SolicitudCreateView, SolicitudListView, SolicitudesPorDoctorView

urlpatterns = [
    path('', SolicitudCreateView.as_view()),
    path('', SolicitudListView.as_view()),
    path('doctor/', SolicitudesPorDoctorView.as_view()),
]
