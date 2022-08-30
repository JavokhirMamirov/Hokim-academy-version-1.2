from django.urls import path, include

urlpatterns = [
    path('admin/', include('api.admin_api.urls')),
    path('student/', include('api.student_api.urls'))
]
