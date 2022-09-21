from django.contrib import admin

# Register your models here.
from home.models import SchoolAriza, TeacherAriza

admin.site.register(SchoolAriza)
admin.site.register(TeacherAriza)