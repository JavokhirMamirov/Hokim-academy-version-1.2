from django.urls import path
from home.viewset.school_view import Dashboard

organization_url = [

]

school_url = [
    path('school/', Dashboard.as_view(), name='school')
]

student_url = [

]

auth_url = [

]

urlpatterns = [

              ] + organization_url + student_url + school_url + auth_url
