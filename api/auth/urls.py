from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.auth.view import get_tokens_for_user, test_view

urlpatterns = [
    path('token/', get_tokens_for_user, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_view, name='token_refresh'),
]
