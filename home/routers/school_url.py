from django.urls import path
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.viewset.school_view import *


school_url = [
    path('school-dashboard/', dashboard, name='school-dashboard'),
    path('student-profile/<int:pk>/', student_profile, name='student-profile'),
    path('teachers/', teachers_view, name='teachers'),
    path('change-student/<int:pk>/', change_student_view, name='change-student'),
    path('add-student/', add_student_view, name='add-student'),
    path('create-student/', create_student, name='create-student'),
    path('abuturient/', abuturient_view, name='abuturient'),
    path('president-student/', president_student_view, name='president-student'),
    path('foreign-student/', foreign_student_view, name='foreign-student'),
    path('settings/', settings_view, name='settings'),
    path('account/', account_view, name='account'),
    path('change-profile/<int:pk>/', change_profile_view, name='change-profile'),

    path('change-school/<int:pk>/', change_school_view, name='change-school'),
    path('change-student-password/<int:pk>/', change_student_password, name='change-student-password'),
    path('delete-student/<int:pk>/', delete_student_view, name='delete-student'),
    path('deleted-students/', deleted_students_view, name='deleted-students'),

]
