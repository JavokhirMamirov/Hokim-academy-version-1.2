import os
from datetime import datetime

import openpyxl
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from HA.settings import BASE_DIR, MEDIA_ROOT
from account.models import School, City, Student, Account
from course.models import WatchHistory, Course, QuizResult
from home.decarators import organ_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import OuterRef, Subquery, Count, Q, IntegerField, Value, Case, When, F, FloatField, \
    ExpressionWrapper, Sum, DecimalField


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    if pages is not None:
        pages = int(pages)
    else:
        pages = 1
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


@login_required(login_url='admin-login')
@organ_required
def student_rating_view(request):
    if request.user.staff == True:
        pages = [20, 50, 100, 200, 500]
        q = request.GET.get('q')
        pagination = request.GET.get('pagination')
        students = Student.objects.filter(active=True, school__isnull=False)
        if q is not None:
            students = students.filter(Q(full_name__icontains=q))

        courses_subquery = WatchHistory.objects.filter(student_id=OuterRef('pk')).values(
            'student').annotate(
            c=Coalesce(Count('*'), Value(0), output_field=IntegerField())).values('c')

        quiz_subquery = QuizResult.objects.filter(student_id=OuterRef('pk'), is_passed=True).values(
            'student').annotate(
            c=Coalesce(Count('*'), Value(0), output_field=IntegerField())).values('c')

        result_subquery = QuizResult.objects.filter(student_id=OuterRef('pk'), is_passed=True).values(
            'student').annotate(
            c=Coalesce(Sum('mark'), Value(0), output_field=FloatField())).values('c')
        students = students.annotate(course=Subquery(courses_subquery), quiz=Subquery(quiz_subquery),
                                     result=Subquery(result_subquery)).annotate(
            mark=Case(
                When(
                    condition=Q(quiz=0) | Q(quiz=None) | Q(course=None),
                    then=0
                ),
                default=ExpressionWrapper(F('result') / F('quiz'),
                                          output_field=DecimalField(max_digits=5, decimal_places=2)),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        )

        students = students.order_by('-mark', '-quiz', '-course')
        if pagination is not None:
            pagination = int(pagination)
        else:
            pagination = 20

        context = {
            "pages": pages,
            "pagination": pagination,
            "students": PagenatorPage(students, pagination, request)
        }
        return render(request, 'oranization/studentRating.html', context)
    else:
        return redirect('organ-dashboard')


@login_required(login_url='admin-login')
@organ_required
def statistics_view(request):
    pages = [20, 50, 100, 200, 500]

    percent_filter = [
        {'value': 1, 'label': "0%-100%"},
        {'value': 2, 'label': "25%-50%"},
        {'value': 3, 'label': "50%-75%"},
        {'value': 4, 'label': "75%-100%"},
        {'value': 5, 'label': "0%"},
        {'value': 6, 'label': "100%"},
        {'value': 7, 'label': "0%-10%"},
        {'value': 8, 'label': "0%-25%"},
    ]
    citys = City.objects.all()
    schools = School.objects.all()
    percent = request.GET.get('percent')

    if percent is None:
        percent = 1
    else:
        try:
            percent = int(percent)
        except:
            percent = 1

    city = request.GET.get('city')
    if city is not None and city != "" and city != '0' and city != 0:
        schools = schools.filter(city_id=city)

    show_count = request.GET.get('show_count')

    if show_count is None or show_count == "" or show_count == '0':
        show_count = 20

    search = request.GET.get('search')
    if search is not None:
        schools.filter(name__icontains=search)

    students = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1, 2, 3]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    student_abt = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[2]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')
    
    student_pr = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    student_cht = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[3]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    students_active = Student.objects.filter(school_id=OuterRef('pk'), is_used_promocode=True, active=True,
                                             status__in=[1, 2, 3]).values(
        'school').annotate(c=Coalesce(Count('*'), Value(0))).values('c')

    schools = schools.annotate(students=Subquery(students), active_student=Subquery(students_active),
        student_abt=Subquery(student_abt), student_pr=Subquery(student_pr), student_cht=Subquery(student_cht)
    ).annotate(
        percent=Case(
            When(
                condition=Q(students__isnull=True) | Q(active_student__isnull=True) | Q(students=0),
                then=0
            ),
            default=ExpressionWrapper((F('active_student') * 100) / F('students'), output_field=FloatField()),
            output_field=FloatField()
        )
    )
    if percent == 1:
        schools = schools.filter(percent__gte=0, percent__lte=100)
    elif percent == 2:
        schools = schools.filter(percent__gte=25, percent__lte=50)
    elif percent == 3:
        schools = schools.filter(percent__gte=50, percent__lte=75)
    elif percent == 4:
        schools = schools.filter(percent__gte=75, percent__lte=100)
    elif percent == 5:
        schools = schools.filter(percent=0)
    elif percent == 6:
        schools = schools.filter(percent=100)
    elif percent == 7:
        schools = schools.filter(percent__gte=0, percent__lte=10)
    else:
        schools = schools.filter(percent__gte=0, percent__lte=25)

    try:
        show_count = int(show_count)
    except:
        show_count = 0

    try:
        city = int(city)
    except:
        city = 0

    try:
        percent = int(percent)
    except:
        percent = 0

    context = {
        'citys': citys,
        'pages': pages,
        'schools': PagenatorPage(schools.order_by('-percent'), show_count, request),
        'percent_filter': percent_filter,
        'show_count': int(show_count),
        'city': int(city),
        'percent': int(percent)
    }
    return render(request, 'oranization/statistics.html', context)


@login_required(login_url='admin-login')
@organ_required
def export_statistics_view(request):
    xslfile = openpyxl.Workbook()
    sheet = xslfile['Sheet']
    sheet['A1'] = "№"
    sheet["B1"] = "Shahar, Tuman"
    sheet['C1'] = "Maktab"
    sheet['D1'] = "O'quvchilar"
    sheet['E1'] = "Faol o'quvchilar"
    sheet['F1'] = "Abuturiyent"
    sheet['G1'] = "Prezident maktabi"
    sheet['H1'] = "Xorijiy til"
    sheet['K1'] = "Foiz"

    schools = School.objects.all()
    percent = request.GET.get('percent')

    if percent is None:
        percent = 1
    else:
        try:
            percent = int(percent)
        except:
            percent = 1

    city = request.GET.get('city')
    if city is not None and city != "" and city != '0' and city != 0:
        schools = schools.filter(city_id=city)

    search = request.GET.get('search')
    if search is not None:
        schools.filter(name__icontains=search)

    students = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1, 2, 3]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')
    
    student_abt = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[2]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')
    
    student_pr = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    student_cht = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[3]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    students_active = Student.objects.filter(school_id=OuterRef('pk'), is_used_promocode=True, active=True,
                                             status__in=[1, 2, 3]).values(
        'school').annotate(c=Coalesce(Count('*'), Value(0))).values('c')

    schools = schools.annotate(students=Subquery(students), active_student=Subquery(students_active),
        student_abt=Subquery(student_abt), student_pr=Subquery(student_pr), student_cht=Subquery(student_cht)).annotate(
        percent=Case(
            When(
                condition=Q(students__isnull=True) | Q(active_student__isnull=True) | Q(students=0),
                then=0
            ),
            default=ExpressionWrapper((F('active_student') * 100) / F('students'), output_field=FloatField()),
            output_field=FloatField()
        )
    )
    if percent == 1:
        schools = schools.filter(percent__gte=0, percent__lte=100)
    elif percent == 2:
        schools = schools.filter(percent__gte=25, percent__lte=50)
    elif percent == 3:
        schools = schools.filter(percent__gte=50, percent__lte=75)
    elif percent == 4:
        schools = schools.filter(percent__gte=75, percent__lte=100)
    elif percent == 5:
        schools = schools.filter(percent=0)
    elif percent == 6:
        schools = schools.filter(percent=100)
    elif percent == 7:
        schools = schools.filter(percent__gte=0, percent__lte=10)
    else:
        schools = schools.filter(percent__gte=0, percent__lte=25)

    schools = schools.order_by('-percent')
    i = 2
    for row in schools:
        sheet[f'A{i}'] = f"{i - 1}"
        sheet[f"B{i}"] = f'{row.city.name}'
        sheet[f'C{i}'] = f"{row.name}"
        sheet[f'D{i}'] = f"{row.students}"
        sheet[f'E{i}'] = f"{row.active_student}"
        sheet[f'F{i}'] = f"{row.student_abt}"
        sheet[f'G{i}'] = f"{row.student_pr}"
        sheet[f'H{i}'] = f"{row.student_cht}"
        sheet[f'K{i}'] = f"{row.percent}"
        i += 1

    f = xslfile.save(os.path.join(MEDIA_ROOT, 'statistics.xlsx'))

    f = open(os.path.join(MEDIA_ROOT, 'statistics.xlsx'), 'rb')

    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(f.read(), content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=statistics.xlsx"
    return response


@login_required(login_url='admin-login')
@organ_required
def day_statistics_view(request):
    if request.user.staff == True:
        pages = [20, 50, 100, 200, 500]

        percent_filter = [
            {'value': 1, 'label': "0%-100%"},
            {'value': 2, 'label': "25%-50%"},
            {'value': 3, 'label': "50%-75%"},
            {'value': 4, 'label': "75%-100%"},
            {'value': 5, 'label': "0%"},
            {'value': 6, 'label': "100%"},
            {'value': 7, 'label': "0%-10%"},
            {'value': 8, 'label': "0%-25%"},
        ]
        citys = City.objects.all()
        schools = School.objects.all()
        percent = request.GET.get('percent')

        if percent is None:
            percent = 1
        else:
            try:
                percent = int(percent)
            except:
                percent = 1

        city = request.GET.get('city')
        if city is not None and city != "" and city != '0' and city != 0:
            schools = schools.filter(city_id=city)

        show_count = request.GET.get('show_count')

        if show_count is None or show_count == "" or show_count == '0':
            show_count = 20

        search = request.GET.get('search')
        if search is not None:
            schools.filter(name__icontains=search)
        date = datetime.now()
        students = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1, 2, 3]).values(
            'school').annotate(
            c=Coalesce(Count('*'), 0)).values('c')

        students_active = Student.objects.filter(school_id=OuterRef('id'), last_login__day=date.day,
                                                 last_login__month=date.month,
                                                 last_login__year=date.year, active=True,
                                                 status__in=[1, 2, 3]).order_by().values(
            'school').annotate(c=Coalesce(Count('*'), Value(0))).values('c')

        schools = schools.annotate(students=Coalesce(Subquery(students), 0),
                                   active_student=Coalesce(Subquery(students_active), 0)).annotate(
            percent=Case(
                When(
                    condition=Q(students__isnull=True) | Q(active_student__isnull=True) | Q(students=0),
                    then=0
                ),
                default=ExpressionWrapper((F('active_student') * 100) / F('students'), output_field=FloatField()),
                output_field=FloatField()
            )
        )
        if percent == 1:
            schools = schools.filter(percent__gte=0, percent__lte=100)
        elif percent == 2:
            schools = schools.filter(percent__gte=25, percent__lte=50)
        elif percent == 3:
            schools = schools.filter(percent__gte=50, percent__lte=75)
        elif percent == 4:
            schools = schools.filter(percent__gte=75, percent__lte=100)
        elif percent == 5:
            schools = schools.filter(percent=0)
        elif percent == 6:
            schools = schools.filter(percent=100)
        elif percent == 7:
            schools = schools.filter(percent__gte=0, percent__lte=10)
        else:
            schools = schools.filter(percent__gte=0, percent__lte=25)

        try:
            show_count = int(show_count)
        except:
            show_count = 0

        try:
            city = int(city)
        except:
            city = 0

        try:
            percent = int(percent)
        except:
            percent = 0

        context = {
            'citys': citys,
            'pages': pages,
            'schools': PagenatorPage(schools.order_by('-active_student'), show_count, request),
            'percent_filter': percent_filter,
            'show_count': int(show_count),
            'city': int(city),
            'percent': int(percent)
        }
        return render(request, 'oranization/day-statistics.html', context)
    else:
        return redirect('organ-dashboard')


@login_required(login_url='admin-login')
@organ_required
def export_day_statistics_view(request):
    date = datetime.today()
    xslfile = openpyxl.Workbook()
    sheet = xslfile['Sheet']
    sheet['A1'] = "№"
    sheet["B1"] = "Shahar, Tuman"
    sheet['C1'] = "Maktab"
    sheet['D1'] = "O'quvchilar"
    sheet['E1'] = "Faol o'quvchilar"
    sheet['F1'] = "Foiz"
    sheet['G1'] = "Sana"

    schools = School.objects.all()
    percent = request.GET.get('percent')

    if percent is None:
        percent = 1
    else:
        try:
            percent = int(percent)
        except:
            percent = 1

    city = request.GET.get('city')
    if city is not None and city != "" and city != '0' and city != 0:
        schools = schools.filter(city_id=city)

    search = request.GET.get('search')
    if search is not None:
        schools.filter(name__icontains=search)

    students = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1, 2, 3]).values(
        'school').annotate(
        c=Coalesce(Count('*'), 0)).values('c')

    students_active = Student.objects.filter(school_id=OuterRef('pk'),
                                             last_login__day=date.day, last_login__month=date.month,
                                             last_login__year=date.year, active=True,
                                             status__in=[1, 2, 3]).order_by().values(
        'school').annotate(c=Coalesce(Count('*'), Value(0))).values('c')

    schools = schools.annotate(students=Coalesce(Subquery(students), 0),
                               active_student=Coalesce(Subquery(students_active), 0)).annotate(
        percent=Case(
            When(
                condition=Q(students__isnull=True) | Q(active_student__isnull=True) | Q(students=0),
                then=0
            ),
            default=ExpressionWrapper((F('active_student') * 100) / F('students'), output_field=FloatField()),
            output_field=FloatField()
        )
    )
    if percent == 1:
        schools = schools.filter(percent__gte=0, percent__lte=100)
    elif percent == 2:
        schools = schools.filter(percent__gte=25, percent__lte=50)
    elif percent == 3:
        schools = schools.filter(percent__gte=50, percent__lte=75)
    elif percent == 4:
        schools = schools.filter(percent__gte=75, percent__lte=100)
    elif percent == 5:
        schools = schools.filter(percent=0)
    elif percent == 6:
        schools = schools.filter(percent=100)
    elif percent == 7:
        schools = schools.filter(percent__gte=0, percent__lte=10)
    else:
        schools = schools.filter(percent__gte=0, percent__lte=25)

    schools = schools.order_by('-active_student')
    i = 2
    for row in schools:
        sheet[f'A{i}'] = f"{i - 1}"
        sheet[f"B{i}"] = f'{row.city.name}'
        sheet[f'C{i}'] = f"{row.name}"
        sheet[f'D{i}'] = f"{row.students}"
        sheet[f'E{i}'] = f"{row.active_student}"
        sheet[f'F{i}'] = f"{row.percent}"
        sheet[f'G{i}'] = f"{date.date()}"
        i += 1

    f = xslfile.save(os.path.join(MEDIA_ROOT, 'statistics.xlsx'))

    f = open(os.path.join(MEDIA_ROOT, 'statistics.xlsx'), 'rb')

    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(f.read(), content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=kunlik-statistika.xlsx"
    return response


@login_required(login_url='admin-login')
@organ_required
def organ_dashboard_view(request):
    schools = School.objects.all().count()
    city = City.objects.all().count()
    students = Student.objects.filter(active=True).count()
    staff = Account.objects.filter(status=3).count()
    abiturent = Student.objects.filter(status=2, active=True).count()
    chet_tili = Student.objects.filter(status=3, active=True).count()
    prez_maktab = Student.objects.filter(status=1, active=True).count()
    teachers = Student.objects.filter(status=4, active=True).count()
    context = {
        'schools': schools,
        'city': city,
        'students': students,
        'staff': staff,
        'abiturent': abiturent,
        'chet_tili': chet_tili,
        'prez_maktab': prez_maktab,
        'teachers': teachers
    }
    return render(request, 'oranization/index.html', context)


@login_required(login_url='admin-login')
@organ_required
def schools_list_view(request):
    pages = [10, 25, 50, 100]
    citys = City.objects.all()
    req = request.GET.get('city')
    q = request.GET.get('q')
    pagination = request.GET.get('pagination')
    schools = School.objects.all()
    if q != '' and q is not None:
        schools = School.objects.filter(Q(name__icontains=q) | Q(director__icontains=q) | Q(address__icontains=q))
    if req != '' and req is not None:
        req = int(req)
        if req == 0:
            schools = School.objects.all()
        else:
            schools = School.objects.filter(city__in=[req])
    else:
        req = 0
    if pagination != '' and pagination is not None:
        pagination = pagination
    else:
        pagination = 10

    students = Student.objects.filter(school_id=OuterRef('pk'), active=True, status__in=[1, 2, 3]).values(
        'school').annotate(c=Count('*')).values('c')

    schools = schools.annotate(students=Subquery(students))

    context = {
        'schools': PagenatorPage(schools.order_by('city_id'), pagination, request),
        'citys': citys,
        'pagination': int(pagination),
        'pages': pages,
        'req': int(req),
    }
    return render(request, 'oranization/schools.html', context)


@login_required(login_url='admin-login')
@organ_required
def add_schools_view(request):
    citys = City.objects.all()
    context = {
        'citys': citys
    }
    if request.method == 'POST':
        name = request.POST['name']
        director = request.POST['director']
        address = request.POST['address']
        city_id = request.POST['city']
        website = request.POST.get('website')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        telegram = request.POST.get('telegram')
        city = City.objects.get(id=city_id)
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        school = School.objects.create(
            name=name,
            director=director,
            address=address,
            city=city,
            lat=lat,
            lng=lng
        )
        if website is not None:
            school.website = website
        if facebook is not None:
            school.facebook = facebook
        if instagram is not None:
            school.instagram = instagram
        if telegram is not None:
            school.telegram = telegram
        school.save()
        return redirect('school-detail', school.id)
    return render(request, 'oranization/add-school.html', context)


@login_required(login_url='admin-login')
@organ_required
def school_detail_view(request, pk):
    school = School.objects.get(pk=pk)
    staff = Account.objects.filter(school=school)
    context = {
        'school': school,
        'staff': staff
    }
    return render(request, 'oranization/school-detail.html', context)


@login_required(login_url='admin-login')
@organ_required
def update_detail_view(request, pk):
    school = School.objects.get(pk=pk)
    citys = City.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        director = request.POST['director']
        address = request.POST['address']
        city_id = request.POST['city']
        website = request.POST.get('website')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        telegram = request.POST.get('telegram')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        city = City.objects.get(id=city_id)
        school.name = name
        school.director = director
        school.address = address
        school.city = city
        school.website = website
        school.facebook = facebook
        school.instagram = instagram
        school.telegram = telegram
        school.save()
        if lat and lng is not None:
            school.lat = lat
            school.lng = lng
            school.save()
        return redirect('school-detail', school.id)
    context = {
        'school': school,
        'citys': citys
    }
    return render(request, 'oranization/update-school.html', context)


@login_required(login_url='admin-login')
@organ_required
def add_staff_school(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            school_id = request.POST['school_id']
            school = School.objects.get(id=school_id)
            users = Account.objects.filter(username=username).count()
            if users > 0:
                messages.error(request, 'Xatolik, Bunday foydalanuvchi mavjud!')
                return redirect('school-detail', school.id)
            else:
                Account.objects.create_user(
                    username=username,
                    password=password,
                    school=school,
                    status=3,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, "Foydalanuvchi muoffaqiyatli yaratilindi!")
                return redirect('school-detail', school.id)
        except:
            messages.error(request, "Foydalanuvchi yaratishda xatolik!")
            return redirect('school-detail', school.id)


@login_required(login_url='admin-login')
@organ_required
def school_delete_view(request, pk):
    school = School.objects.get(id=pk)
    school.delete()
    return redirect('schools')


@login_required(login_url='admin-login')
@organ_required
def user_detail_view(request, pk):
    account = Account.objects.get(id=pk)
    schools = School.objects.all()
    context = {
        'account': account,
        'schools': schools
    }
    return render(request, 'oranization/user-detail.html', context)


@login_required(login_url='admin-login')
@organ_required
def user_update_view(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        school_id = request.POST['school']
        school = School.objects.get(id=school_id)
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        users = Account.objects.filter(username=username).count()
        if users > 0 and account.username != username:
            messages.error(request, 'Xatolik, Bunday foydalanuvchi mavjud!')
            return redirect('user-detail', account.id)
        else:
            account.username = username
            account.first_name = first_name
            account.last_name = last_name
            account.school = school
            account.save()
            return redirect('user-detail', account.id)
    return render(request, 'oranization/user-detail.html')


@login_required(login_url='admin-login')
@organ_required
def user_set_password(request, pk):
    user = Account.objects.get(pk=pk)
    if request.method == 'POST':
        password = request.POST['password']
        password_2 = request.POST['password2']
        if password == password_2:
            user.set_password(password)
            user.save()
            messages.success(request, "Foydalanuvchi paroli o`zgartirildi!")
            return redirect('user-detail', user.id)
        else:
            messages.error(request, "Parollar bir xil emas!")
            return redirect('user-detail', user.id)
    else:
        return redirect('user-detail', user.id)


@login_required(login_url='admin-login')
@organ_required
def user_delete_view(request, pk):
    user_del = Account.objects.get(pk=pk)
    school = School.objects.get(id=user_del.school.id)
    user_del.delete()
    return redirect('school-detail', school.id)
