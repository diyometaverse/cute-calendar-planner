from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, "dashboard.html", {"active": "dashboard"})

def calendar_view(request):
    return render(request, "calendar.html", {"active": "calendar"})

def files_view(request):
    return render(request, "files.html", {"active": "files"})