from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset.school_view import *


school_url = [
    path('school-dashboard/', Dashboard, name='school-dashboard'),
    path('teacher-profile/<int:pk>/', TeacherProfile, name='teacher-profile'),
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('change-teacher/<int:pk>/', ChangeTeacher, name='change-teacher'),
    path('add-teacher/', AddTeacher.as_view(), name='add-teacher'),
]