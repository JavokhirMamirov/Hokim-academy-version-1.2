from django.urls import path

from api.teacher_api import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', api_views.studentLoginView),
    path('change-password/', api_views.changePasswordView),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
