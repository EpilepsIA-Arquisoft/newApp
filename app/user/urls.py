from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    LogoutView,
    CurrentUserView,
    DoctorDashboardView,
    BotReducerTaskView,
    BotExamenUploaderTaskView,
    AdminPanelView,
    AdminListUsersView
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    #path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    #path('bot/reducer/task/', BotReducerTaskView.as_view(), name='bot_reducer_task'),
    #path('bot/examen-uploader/task/', BotExamenUploaderTaskView.as_view(), name='bot_examen_uploader_task'),
    #path('user/', AdminListUsersView.as_view(), name='admin_panel'),
]
