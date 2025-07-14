from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProjectForm, TaskForm, UserForm, CustomInviteSignupForm
from .models import Project, UserProfile, Task
from .notify import send_email, send_message
from datetime import date

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

def update_tasks(req):
    if req.method == "GET":
        tasks = Task.objects.all()
        profile = UserProfile.objects.get(user__username=req.user.username)
        return render(req, "tasks.html", {"tasks": tasks, "profile": profile})
    
    if req.method == "POST":
        # 'completed_tasks' could be a single value or a list
        completed_ids = req.POST.getlist('completed_tasks')
        user_profile = UserProfile.objects.get(user=req.user)
        for task_id in completed_ids:
            try:
                task = Task.objects.get(id=task_id)
                user_profile.tasks.remove(task)  # Remove task from user profile (not delete)
            except Task.DoesNotExist:
                continue
        messages.success(req, "Completed tasks removed!")
    
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
                            if "whatsapp" in task.notify:
                                wa_message = (
                                                f"🟢 *Uruk GC Task Assigned*\n\n"
                                                f"*Project:* {task.project.project_name if task.project else 'N/A'}\n"
                                                f"*Task:* {task.title}\n"
                                                f"*Due Date:* {task.due_date.strftime('%B %d, %Y')}\n\n"
                                                f"*Description:*\n{task.desc}\n\n"
                                                f"Please check your dashboard for more details."
                                            )

                                send_message(profile.phone, wa_message)
                            if "email" in task.notify:
                                email_html = f"""
                                                <html>
                                                <body style="font-family: 'Open Sans', Arial, sans-serif; background: #fafbfc; color: #222; padding: 0; margin: 0;">
                                                    <div style="max-width: 500px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 20px #0001; padding: 36px 32px;">
                                                    <div style="text-align: center; margin-bottom: 24px;">
                                                        <h1> Uruk GC  </h2>
                                                    </div>
                                                    <h2 style="color: #800000; margin-top: 0; margin-bottom: 12px;">New Task Assigned</h2>
                                                    <div style="margin-bottom: 22px;">
                                                        <strong style="color:#222;">Hello {user.first_name}, please complete the following task assigned to you:<br><br>
                                                        <strong style="color:#222;">Project:</strong> {task.project.project_name if task.project else 'N/A'}<br>
                                                        <strong style="color:#222;">Task:</strong> {task.title}<br>
                                                        <strong style="color:#222;">Due Date:</strong> {task.due_date.strftime('%B %d, %Y')}
                                                    </div>
                                                    <div style="margin-bottom: 22px;">
                                                        <strong style="color:#222;">Description:</strong><br>
                                                        <span style="color:#555;">{task.desc}</span>
                                                    </div>
                                                    <div style="margin-top: 32px; color: #888; font-size: 13px; text-align: center;">
                                                        © {date.today().year} Uruk GC
                                                    </div>
                                                    </div>
                                                </body>
                                                </html>
                                                """

                                send_email("umairarhambd@gmail.com", [user.email], email_html)
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


def signup(request): 
    if request.method == 'POST':
        form = CustomInviteSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')
    else:
        form = CustomInviteSignupForm()
    return render(request, 'signup.html', {'signup_form': form})









