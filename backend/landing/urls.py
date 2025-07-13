from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login_user, name="login_user"),
    path('log_out/', views.log_out, name="log_out"),
    path('home/', views.home, {'name': 'home'}, name="home"),
    path('calendar/', views.home, {'name': 'calendar'}, name="calendar"),
    path('projects/', views.get_projects, name="projects"),
    path('tasks/', views.update_tasks, name="tasks"),
    path('profile/', views.profile, name="profile"),
    # path('admin_page/', views.home, {'name': 'admin_page'}, name="admin_page"),
    path('admin_page/', views.admin_page, name="admin_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)