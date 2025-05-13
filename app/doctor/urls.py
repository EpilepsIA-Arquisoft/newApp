from django.urls import path
from .views import DoctorListView, DoctorCreateView

urlpatterns = [
    path('', DoctorListView.as_view()),
    #path('', DoctorCreateView.as_view()),
    
]
