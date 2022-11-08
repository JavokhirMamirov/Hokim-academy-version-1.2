import datetime
import random

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from account.models import Student, School, Attendance
from course.models import Course
from home.decarators import admin_required


def chart_data(request):
    date = datetime.datetime.today()
    visit_today = Attendance.objects.filter(date=date.date()).count()
    data_vists = []
    data_days = []
    for i in range(6, 0, -1):
        d = date - datetime.timedelta(days=i)
        vs = Attendance.objects.filter(date=d.date()).count()
        data_days.append(d.date())
        data_vists.append(vs)

    data_days.append(date.date())
    data_vists.append(visit_today)

    data = {
        "days": data_days,
        "visits": data_vists,
    }

    return JsonResponse(data)


@login_required(login_url='admin-login')
@admin_required
def dashboardView(request):
    date = datetime.datetime.today()
    courses = Course.objects.filter(is_active=True, step=7)
    total_students = Student.objects.filter(active=True).count()
    schools = School.objects.all().count()
    online_number = random.randint(900, 2000)
    ab = Student.objects.filter(active=True, status=2).count()
    pr = Student.objects.filter(active=True, status=1).count()
    xr = Student.objects.filter(active=True, status=3).count()
    tch = Student.objects.filter(active=True, status=4).count()
    visit_today = Attendance.objects.filter(date=date.date()).count()
    data_vists = []
    data_days = []
    for i in range(6, 0, -1):
        d = date - datetime.timedelta(days=i)
        vs = Attendance.objects.filter(date=d.date()).count()
        data_days.append(d.date())
        data_vists.append(vs)

    data_days.append(date.date())
    data_vists.append(visit_today)

    context = {
        "courses": courses[0:10],
        "total_students": total_students,
        "schools": schools,
        "online_number": online_number,
        "ab": ab,
        "pr": pr,
        "xr": xr,
        "tch": tch,
        "today_visit": visit_today,
        "data_day": data_days,
        "data_visit": data_vists
    }
    return render(request, 'superadmin/index.html', context)
