import io
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
import json, datetime as dt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from planner.forms import ClientForm, FileUploadForm
from planner.utils.supabase import delete_file_from_supabase, get_supabase_public_url, upload_file_to_supabase
from .models import Client, Event, File, UserProfile
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from planner.utils.google_drive import upload_to_google_drive
import mimetypes
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
    clients = Client.objects.filter(user=request.user, is_active=True)
    events_json = json.dumps(list(events), cls=DjangoJSONEncoder)
    return render(
        request,
        "calendar.html",
        {
            "active": "calendar",
            "events_json": events_json,
            'clients': clients
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
            if user.is_superuser:
                return redirect('/admin/')
            return redirect("planner:dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def logout_user(request):
    request.session.flush()  
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    messages.success(request, "Thank you! ❤️")
    return redirect("login")

def dashboard(request):
    events = Event.objects.filter(user=request.user).order_by("start")
    return render(request, "planner/dashboard.html", {"events": events})

def files_page(request):
    files = File.objects.filter(user=request.user).order_by('-uploaded_at')

    for f in files:
        ext = os.path.splitext(f.file.name)[1].lower()
        f.file_ext = ext

    form = FileUploadForm()
    return render(request, 'files.html', {
        'form': form,
        'files': files,
        'active': "files"
    })

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            filename = uploaded_file.name
            file_ext = os.path.splitext(filename)[1].lower()
            username = request.user.username

            office_exts = ['.doc', '.docx', '.xls', '.xlsx']

            if file_ext in office_exts:
                try:
                    drive_url = upload_to_google_drive(
                        io.BytesIO(uploaded_file.read()),
                        filename,
                        uploaded_file.content_type,
                        username
                    )
                except Exception as e:
                    return JsonResponse({'success': False, 'error': f'Google Drive Error: {str(e)}'}, status=500)

                external_url = drive_url

            else:
                upload_result = upload_file_to_supabase(uploaded_file, path=username)
                if "error" in upload_result:
                    return JsonResponse({'success': False, 'error': upload_result["error"]}, status=500)

                external_url = upload_result["public_url"]

            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.file = uploaded_file
            file_instance.external_url = external_url
            file_instance.save()

            return JsonResponse({'success': True, 'url': external_url})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def get_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)

    return JsonResponse({
        'id': file.id,
        'title': file.title,
        'description': file.description,
        'date': file.date.isoformat() if file.date else None,
        'external_url': file.external_url
    })

@login_required
def edit_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            if 'file' in request.FILES:
                if file.external_url:
                    delete_file_from_supabase(file.external_url)

                uploaded_file = request.FILES['file']
                upload_result = upload_file_to_supabase(uploaded_file, path=request.user.username)
                if "error" in upload_result:
                    return JsonResponse({'success': False, 'error': upload_result["error"]}, status=500)

                file.external_url = upload_result["public_url"]

            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def delete_file(request, file_id):
    if request.method == 'POST':
        file = get_object_or_404(File, id=file_id, user=request.user)

        if file.external_url:
            delete_file_from_supabase(file.external_url)

        file.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def settings_page(request):
    user = request.user
    clients = user.clients.all()
    profile = UserProfile.objects.filter(user=user).first()

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        if 'profile_image' in request.FILES:
            uploaded_image = request.FILES['profile_image']
            upload_result = upload_file_to_supabase(uploaded_image, f"profile_images/{user.username}")

            if upload_result and not upload_result.get("error"):
                public_url = upload_result["public_url"]  # ✅ Just use the public_url directly

                if profile:
                    profile.profile_image_url = public_url
                    profile.save()
                else:
                    UserProfile.objects.create(
                        user=user,
                        profile_image_url=public_url
                    )
            else:
                return JsonResponse({'success': False, 'message': upload_result.get("error")}, status=400)

        messages.success(request, "Profile updated successfully 💖")
        return JsonResponse({'success': True})

    return render(request, 'settings.html', {
        'user': user,
        'active': "settings",
        'profile': profile,
        'clients': clients
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return JsonResponse({
                'success': True,
                'client': {
                    'id': client.id,
                    'name': client.name,
                    'email': client.email,
                    'phone': client.phone,
                    'created_at': client.created_at.strftime('%b %d, %Y')
                }
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def edit_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id, user=request.user)
    except Client.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Client not found'}, status=404)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                'success': True,
                'client': client.get_full_details()
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def delete_client(request, client_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=client_id, user=request.user)
            client.delete()
            return JsonResponse({'success': True})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def get_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id, user=request.user)
        return JsonResponse(client.get_full_details())
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    
@login_required
def toggle_client_active(request, client_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=client_id, user=request.user)
            client.is_active = not client.is_active
            client.save()
            return JsonResponse({
                'success': True,
                'is_active': client.is_active
            })
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def change_password(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        return JsonResponse({
            'success': False, 
            'message': 'All fields are required'
        }, status=400)

    if new_password != confirm_password:
        return JsonResponse({
            'success': False, 
            'message': 'New passwords do not match'
        }, status=400)

    user = request.user
    if not user.check_password(current_password):
        return JsonResponse({
            'success': False, 
            'message': 'Current password is incorrect'
        }, status=400)

    try:
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({
            'success': True, 
            'message': 'Password updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Failed to update password'
        }, status=500)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method == 'POST':
        try:
            event.title = request.POST.get('title')
            event.desc = request.POST.get('desc', '')
            event.start = request.POST.get('start')
            event.end = request.POST.get('end') or None
            event.client = request.POST.get('client', '')
            event.priority = request.POST.get('priority')
            event.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id, user=request.user)
        event.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

@login_required
def calendar_list_view(request):
    today = timezone.now().date()
    
    events = Event.objects.filter(user=request.user, start__gte=today).order_by('start')
    clients = Client.objects.filter(user=request.user, is_active=True)
    return render(request, 'calendar_list.html', {
        'events': events,
        'clients': clients,
        'active': 'calendar'
    })