from django.urls import path

from api.teacher_api import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('language/', api_views.languageView),
    path('course-status/', api_views.courseStatusView),
    path('level/', api_views.levelView),
    path('category/', api_views.categoryView),
    path('sub-category/', api_views.subCategoryView),
    path('tag/', api_views.tagView),

    path('course/', api_views.courseView),
    path('course/<int:pk>/', api_views.courseView)

]

auth_patterns = [
    path('login/', api_views.teacherLoginView),
    path('change-password/', api_views.changePasswordView),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = urlpatterns + auth_patterns
