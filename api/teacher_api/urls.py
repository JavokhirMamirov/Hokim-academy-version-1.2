from django.urls import path

from api.teacher_api import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('language/', api_views.languageView),
    path('course-status/', api_views.courseStatusView),
    path('level/', api_views.levelView),
    path('category/', api_views.categoryView),
    path('tag/', api_views.tagView),

    path('course/', api_views.courseView),
    path('course/<int:pk>/', api_views.courseView),
    path('section/', api_views.sectionView),
    path('section/quiz/<int:pk>/', api_views.quizSectionView),
    path('section/<int:pk>/', api_views.sectionView),
    path('lesson/', api_views.lessonView),
    path('lesson/<int:pk>/', api_views.lessonView),
    path('quiz/', api_views.quizView),
    path('quiz/result/', api_views.quizResultView),
    path('quiz/<int:pk>/', api_views.quizView),
    path('question/', api_views.questionView),
    path('question/<int:pk>/', api_views.questionView),
    path('attachment/', api_views.courseAttachmentView),
    path('attachment/<int:pk>/', api_views.courseAttachmentView),
    path('course-step/<int:pk>/', api_views.changeCourseStep),
    path('my-courses/', api_views.myCourseView),
    path('my-courses/<int:pk>/', api_views.myCourseView),
    path('my-students/', api_views.myStudentsView),

    path('dashboard/', api_views.myDashboardView),
    path('change-image/', api_views.changeTeacherImageView),
    path('change-video/', api_views.changeTeacherVideoView),
    path('check-username/', api_views.checkUsernameView),
    path('profile/', api_views.teacherView),
    path('course/detail/<int:pk>/', api_views.detailCourseView),
    path('course/comments/<int:pk>/', api_views.commentsView),

]

auth_patterns = [
    path('login/', api_views.teacherLoginView),
    path('change-password/', api_views.changePasswordView),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = urlpatterns + auth_patterns
