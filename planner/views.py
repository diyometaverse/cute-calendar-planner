from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json, datetime as dt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Event
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
# Create your views here.

def index(request):
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    today = timezone.now().date()

    events = (
        Event.objects
             .filter(user=request.user, start__gte=today)
             .order_by("start")
    )

    return render(
        request,
        "dashboard.html",
        {"active": "dashboard", "events": events},
    )

@login_required
def calendar_view(request):
    events = Event.objects.filter(user=request.user).values("start","priority","title","desc","client")
    events_json = json.dumps(list(events), cls=DjangoJSONEncoder)
    return render(
        request,
        "calendar.html",
        {
            "active": "calendar",
            "events_json": events_json,
        },
    )

def files_view(request):
    return render(request, "files.html", {"active": "files"})

@login_required
def create_event(request):
    if request.method == "POST":
        try:
            payload  = json.loads(request.body or "{}")
            event = Event.objects.create(
                user     = request.user,
                title    = payload["title"],
                desc     = payload.get("desc", ""),
                start    = payload["start"],
                end      = payload.get("end") or None,
                client   = payload.get("client", ""),
                priority = payload.get("priority", "mid"),
            )
            return JsonResponse({"id": event.id}, status=201)
        except (KeyError, ValueError) as exc:
            return HttpResponseBadRequest(f"Bad request: {exc}")

    return HttpResponseBadRequest("Only POST is allowed")
    
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("planner:dashboard")
        messages.error(request, "Invalid credentials")

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "Thank you for using, I love you! ❤️")
    return redirect("login")

def dashboard(request):
    events = Event.objects.filter(user=request.user).order_by("start")
    return render(request, "planner/dashboard.html", {"events": events})