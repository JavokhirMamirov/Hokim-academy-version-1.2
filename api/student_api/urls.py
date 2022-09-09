from django.urls import path

from api.student_api import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', api_views.studentLoginView),
    path('change-password/', api_views.changePasswordView),
    path('change-password-first/', api_views.changePasswordAndUsernameFirstView),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('course-home/', api_views.bestThreeAndRecomCourseView),
    path('courses/', api_views.allCourseView),

    path('category/', api_views.categoryView),
    path('level/', api_views.levelView),
    path('course-status/', api_views.courseStatusView),

    path('profile/', api_views.studentView),
    path('change-image/', api_views.changeStudentImageView),
    path('check-username/', api_views.checkUsernameView)
]
