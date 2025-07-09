from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name="login_user"),
    path('log_out/', views.log_out, name="log_out"),
    path('home/', views.home, {'name': 'home'}, name="home"),
    path('calendar/', views.home, {'name': 'calendar'}, name="calendar"),
    path('projects/', views.home, {'name': 'projects'}, name="projects"),
    path('tasks/', views.home, {'name': 'tasks'}, name="tasks"),
    path('profile/', views.home, {'name': 'profile'}, name="profile"),
    path('admin/', views.home, {'name': 'admin'}, name="admin"),
]
