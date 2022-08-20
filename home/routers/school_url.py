from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset.school_view import *


school_url = [
    path('school-dashboard/', dashboard, name='school-dashboard'),
    path('teacher-profile/<int:pk>/', teacher_profile, name='teacher-profile'),
    path('teachers/', teachers_view, name='teachers'),
    path('change-teacher/<int:pk>/', change_teacher_view, name='change-teacher'),
    path('add-teacher/', add_teachers_view, name='add-teacher'),
    path('create-teacher/', create_teacher, name='create-teacher'),

]