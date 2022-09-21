from django.urls import path, include
from home.viewset.auth_view import admin_login, admin_logout, page_404
from home.routers.organ_url import organization_url
from home.routers.school_url import school_url
from home.routers.admin_url import admin_urlpattern

auth_url = [
    path('', admin_login, name='admin-login'),
    path('logout/', admin_logout, name='admin-logout'),
    path('404/', page_404, name='page-404')
]

urlpatterns = [
    path('school/', include(school_url)),
    path('organ/', include(organization_url)),
    path('superadmin/', include(admin_urlpattern)),
    path('', include(auth_url))

  ]
