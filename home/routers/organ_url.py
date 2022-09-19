from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset import organization_vew

organization_url = [

    path('dashboard/', organization_vew.organ_dashboard_view, name='organ-dashboard'),
    path('schools/', organization_vew.schools_list_view, name='schools'),
    path('school/add/', organization_vew.add_schools_view, name='add-school'),
    path('staff/add/', organization_vew.add_staff_school, name='staff-add'),
    path('school/detail/<int:pk>/', organization_vew.school_detail_view, name='school-detail'),
    path('school/update/<int:pk>/', organization_vew.update_detail_view, name='update-school'),
    path('user/delete/<int:pk>/', organization_vew.user_delete_view, name='user-delete'),
    path('user/<int:pk>/', organization_vew.user_detail_view, name='user-detail'),
    path('user/update/<int:pk>/', organization_vew.user_update_view, name='user-update'),
    path('user/password/set/<int:pk>/', organization_vew.user_set_password, name='user-change-password'),
    path('school/delete/<int:pk>/', organization_vew.school_delete_view, name='delete-school'),
    path('statistics/', organization_vew.statistics_view, name='school-statistics'),
]