"""
URL configuration for project_calendar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'planner'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('calendar/', views.calendar_view,  name='calendar'),
    path("calendar/create/", views.create_event, name="event-create"),
    path('calendar/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('calendar/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('files/', views.files_page, name='files'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/<int:file_id>/', views.get_file, name='get_file'),
    path('files/<int:file_id>/edit/', views.edit_file, name='edit_file'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('settings/', views.settings_page, name='settings'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/<int:client_id>/', views.get_client, name='get_client'),
    path('clients/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    path('clients/<int:client_id>/toggle-active/', views.toggle_client_active, name='toggle_client_active'),
    path('calendar/list/', views.calendar_list_view, name='calendar_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)