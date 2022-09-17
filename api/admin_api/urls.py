from django.urls import path, include
from api.admin_api import routers
from . import api_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', include(routers.urlpatterns)),
    path('login/', api_view.admin_login_view),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/', api_view.infoView),
    path('prize/', api_view.prizeView)
]
