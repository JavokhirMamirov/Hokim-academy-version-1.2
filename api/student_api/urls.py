from django.urls import path

from api.student_api import api_views

urlpatterns = [
    path('login/', api_views.studentLoginView),
    path('change-password/<int:pk>/', api_views.changePasswordView),
    path('change-password-first/<int:pk>/', api_views.changePasswordAndUsernameFirstView)
]
