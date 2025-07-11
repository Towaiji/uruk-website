from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .supabase_client import get_supabase_client
from django.http import HttpResponseRedirect
from .forms import ProjectForm, TaskForm, UserForm
from .models import Project, UserProfile, Task

def home(req, name="home"):  # Default to "home" for the root

    return render(req, f"{name}.html", {})

def profile(req):  # Default to "home" for the root
    profile = UserProfile.objects.get(user__username=req.user.username)
    return render(req, "profile.html", {"profile": profile})

def login_user(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "There was an error logging in, please try again")
            return redirect('login_user')

    return render(req, "login_user.html", {})

def log_out(req):
    logout(req)
    messages.error(req, "You were successfully logged out!")
    return redirect('login_user')


def get_projects(req):
    if req.method == "GET":
        projects = Project.objects.all()
        profile = UserProfile.objects.get(user__username=req.user.username)
        return render(req, "projects.html", {"projects": projects, "profile": profile})
    
    return render(req, "projects.html", {})

def get_tasks(req):
    if req.method == "GET":
        tasks = Task.objects.all()
        profile = UserProfile.objects.get(user__username=req.user.username)
        return render(req, "tasks.html", {"tasks": tasks, "profile": profile})
    
    return render(req, "tasks.html", {})

def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully.")
            return redirect('admin_page')  # reload the same page

    else:
        form = ProjectForm()

    return render(request, "admin_page.html", {"form": form})


def admin_page(request):
    project_form = ProjectForm()
    task_form = TaskForm()
    user_filter_form = UserForm(request.GET or None)
    users = User.objects.all()
    projects = Project.objects.all()
    profile = UserProfile.objects.get(user__username=request.user.username)

    # For user search/filtering
    if request.GET and 'search_user' in request.GET:
        user_filter_form = UserForm(request.GET)
        if user_filter_form.is_valid():
            # Filter users here, for example:
            name = user_filter_form.cleaned_data['name']
            if name:
                users = users.filter(username__icontains=name)
            # ...add other filters as needed

    # For POST (add project or assign task)
    if request.method == "POST":
        if "add_project" in request.POST:
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project_form.save()
                messages.success(request, "Project added successfully.")
                return redirect('admin_page')

        # assigning tasks to user
        elif "assign_task" in request.POST:
            task_form = TaskForm(request.POST)

            if task_form.is_valid():
                
                task = task_form.save()
                selected_users = task_form.cleaned_data['assigned_users']  # a QuerySet of User objects
                if not selected_users:
                    messages.error(request, "No user selected.")
                else:
                    # For each user, add the task to their UserProfile.tasks
                    print("Assign task reached and task form found to be valid \n\n\n\n\n\n\n\n")
                    print(selected_users)
                    for user in selected_users:
                        try:
                            profile = UserProfile.objects.get(user=user)
                            profile.tasks.add(task)
                        except UserProfile.DoesNotExist:
                            messages.error(request, f"Profile for {user.username} not found!")
                    messages.success(request, "Task assigned.")

                return redirect('admin_page')
            
            else:
                print("Task form errors:", task_form.errors)

    context = {
        "project_form": project_form,
        "task_form": task_form,
        "user_filter_form": user_filter_form,
        "users": users,
        "projects": projects,
        "profile": profile,
    }
    return render(request, "admin_page.html", context)










