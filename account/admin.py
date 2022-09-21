from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Skill)
admin.site.register(City)
admin.site.register(Info)
admin.site.register(Prize)
admin.site.register(Region)


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
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
