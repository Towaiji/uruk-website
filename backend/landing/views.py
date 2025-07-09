from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(req, name="home"):  # Default to "home" for the root
    return render(req, f"{name}.html", {})

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
    print("MY LOGOUT VIEW CALLED")
    messages.error(req, "You were successfully logged out!")
    return redirect('login_user')