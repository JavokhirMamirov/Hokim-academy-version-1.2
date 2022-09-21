import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import Student, School
from course.models import Course
from home.decarators import admin_required


@login_required(login_url='admin-login')
@admin_required
def dashboardView(request):
    courses = Course.objects.filter(is_active=True, step=7)
    total_students = Student.objects.filter(active=True).count()
    schools = School.objects.all().count()
    online_number = random.randint(900, 2000)
    ab = Student.objects.filter(active=True, status=2).count()
    pr = Student.objects.filter(active=True, status=1).count()
    xr = Student.objects.filter(active=True, status=3).count()
    tch = Student.objects.filter(active=True, status=4).count()
    context = {
        "courses": courses[0:10],
        "total_students": total_students,
        "schools": schools,
        "online_number": online_number,
        "ab":ab,
        "pr":pr,
        "xr":xr,
        "tch":tch
    }
    return render(request, 'superadmin/index.html', context)
