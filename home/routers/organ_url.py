from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset.organization_vew import organ_dashboard_view

organization_url = [

    path('dashboard/', organ_dashboard_view, name='organ-dashboard')

]