from django.urls import path
from ..viewset import admin_viewset

admin_urlpattern = [
    path('dashboard/', admin_viewset.dashboardView, name='admin-dashboard')
]
