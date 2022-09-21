from django.urls import path
from api.website import api_view

urlpatterns = [
    path('school-ariza/', api_view.postSchoolAriza),
    path('teacher-ariza/', api_view.postTeacherAriza),
    path('region/', api_view.regionView),
    path('city/', api_view.cityView),
]