from django.urls import path
from api.bot_api import api_view
urlpatterns = [
    path('login/', api_view.studentLoginView),
    path('logout/', api_view.studentLogOut),
    path('courses/', api_view.myCoursesView),
    path('quiz/', api_view.quizView),
    path('quiz/<int:pk>/', api_view.quizView),
    path('quiz/result/', api_view.get_quiz_result_view),
    path('quiz/question/', api_view.question_view),
]