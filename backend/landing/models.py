from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    completion_date = models.DateField()
    services = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_users = models.ManyToManyField(User, related_name='users', blank=True) 

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)  
    role = models.CharField(max_length=255, blank=True)
    projects = models.ManyToManyField(Project, related_name='users', blank=True)  # ManyToMany if users can be on multiple projects
    tasks = models.ManyToManyField(Task, related_name='users', blank=True) 

    def __str__(self):
        return self.user.username
