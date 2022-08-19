from django.urls import path
from home.viewset.school_view import *

organization_url = [

]

school_url = [
    path('school-dashboard/', Dashboard.as_view(), name='school-dashboard'),
    path('teacher-profile/<int:pk>/', TeacherProfile.as_view(), name='teacher-profile'),
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('change-teacher/<int:pk>/', ChangeTeacher, name='change-teacher'),
    path('add-teacher/', AddTeacher.as_view(), name='add-teacher'),
]

student_url = [

]

auth_url = [

]

urlpatterns = [

              ] + organization_url + student_url + school_url + auth_url
