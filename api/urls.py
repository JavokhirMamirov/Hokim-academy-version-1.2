from django.urls import path, include

urlpatterns = [
    path('admin/', include('api.admin_api.urls')),
    path('student/', include('api.student_api.urls')),
    path('teacher/', include('api.teacher_api.urls')),
    path('website/', include('api.website.urls')),
    path('bot/', include('api.bot_api.urls')),
]
