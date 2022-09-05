from django.urls import path

from api.student_api import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', api_views.studentLoginView),
    path('change-password/', api_views.changePasswordView),
    path('change-password-first/', api_views.changePasswordAndUsernameFirstView),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
