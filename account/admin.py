from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.
# admin.site.register(Student)
# admin.site.register(School)
admin.site.register(Skill)
# admin.site.register(City)
admin.site.register(Info)
admin.site.register(Prize)
admin.site.register(Attendance)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'username']
    search_fields = ['full_name']
    list_filter = ['is_active']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'director', 'address']
    search_fields = ['name']
    list_filter = ['city']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['region']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'school']
    row_id_fields = ('school',)
    search_fields = ['full_name']
    list_filter = ['active', 'status']


@admin.register(Account)
class AccountAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "status",
                    'school',
                    "groups",
                    "staff",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
