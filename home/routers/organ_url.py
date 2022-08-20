from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset import organization_vew

organization_url = [

    path('dashboard/', organization_vew.organ_dashboard_view, name='organ-dashboard'),
    path('schools/', organization_vew.schools_list_view, name='schools'),
    path('school/add/', organization_vew.add_schools_view, name='add-school'),
    path('school/detail/<int:pk>/', organization_vew.school_detail_view, name='school-detail'),
    path('school/update/<int:pk>/', organization_vew.update_detail_view, name='update-school')

]