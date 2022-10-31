from django.urls import path
from api.bot_api import api_view
urlpatterns = [
    path('login/', api_view.studentLoginView),
    path('logout/', api_view.studentLogOut),
]