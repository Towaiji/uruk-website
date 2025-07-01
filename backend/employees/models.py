from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    date_hired = models.DateField()
    projects = models.ManyToManyField('projects.Project', related_name='employees', blank=True)

    def __str__(self):
        return self.name
