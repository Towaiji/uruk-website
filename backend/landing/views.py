from django.shortcuts import render

def home(req, name="home"):  # Default to "home" for the root
    return render(req, f"{name}.html", {})
