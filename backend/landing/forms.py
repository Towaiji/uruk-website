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

class CustomInviteSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def save(self):
        # Create user
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password'],
        )
        # Create linked profile
        UserProfile.objects.create(
            user=user,
            phone=self.cleaned_data['phone']
        )
        return user