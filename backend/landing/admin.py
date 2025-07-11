from django.contrib import admin
from .models import Project, Task, UserProfile

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(UserProfile)