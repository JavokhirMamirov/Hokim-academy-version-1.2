from django.urls import path, include

from home.viewset.auth_view import admin_login, admin_logout
from home.viewset.organization_vew import organ_dashboard_view
from home.viewset.school_view import *

organization_url = [

    path('dashboardd/', organ_dashboard_view, name='organ-dashboard')

]

school_url = [
    path('school-dashboard/', Dashboard.as_view(), name='school-dashboard'),
    path('teacher-profile/<int:pk>/', TeacherProfile.as_view(), name='teacher-profile'),
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('change-teacher/<int:pk>/', ChangeTeacher, name='change-teacher'),
    path('add-teacher/', AddTeacher.as_view(), name='add-teacher'),
]

student_url = [
    path()
]

auth_url = [
    path('login/', admin_login, name='admin-login'),
    path('logout/', admin_logout, name='admin-logout')
]

urlpatterns = [
    path('school/', include(school_url)),
    path('organ/', include(organization_url)),
    path('student/', include(student_url)),
    path('auth/', include(auth_url))

  ]
