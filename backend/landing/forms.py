from django import forms
from django.forms import ModelForm
from .models import Project, Task, UserProfile
from django.contrib.auth.models import User

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
    
class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"