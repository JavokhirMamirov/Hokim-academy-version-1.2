from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from account.models import *
from django.contrib.auth.decorators import login_required
from home.decarators import school_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


@login_required(login_url='admin-login')
@school_required
def dashboard(request):
    school = request.user.school
    context = {
        'pupil_count': Student.objects.filter(status__in=[1, 2, 3], school=school).count(),
        'for_president_school_count': Student.objects.filter(status=1, school=school).count(),
        'abuturient_count': Student.objects.filter(status=2, school=school).count(),
        'foreigners_count': Student.objects.filter(status=3, school=school).count(),
        'teacher_count': Student.objects.filter(status=4, school=school).count(),
    }
    return render(request, 'school/index.html', context)


@login_required(login_url='admin-login')
@school_required
def student_profile(request, pk):
    context = {
        'teacher': Student.objects.get(id=pk),
        'subject': Subject.objects.all()
    }
    return render(request, 'school/student-profile.html', context)


@login_required(login_url='admin-login')
@school_required
def teachers_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        teacher = Student.objects.filter(status=4, school=request.user.school)
    else:
        teacher = Student.objects.filter(status=4, school=request.user.school, full_name__icontains=search)
    context = {
        'teachers': PagenatorPage(teacher, 50, request)
    }
    return render(request, 'school/teachers.html', context)


@login_required(login_url='admin-login')
@school_required
def abuturient_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        abuturient = Student.objects.filter(status=2, school=request.user.school)
    else:
        abuturient = Student.objects.filter(status=2, school=request.user.school, full_name__icontains=search)
    context = {
        'abuturient': PagenatorPage(abuturient, 50, request)
    }
    return render(request, 'school/abuturient.html', context)


@login_required(login_url='admin-login')
@school_required
def foreign_student_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        student = Student.objects.filter(status=3, school=request.user.school)
    else:
        student = Student.objects.filter(status=3, school=request.user.school, full_name__icontains=search)
    context = {
        'student': PagenatorPage(student, 50, request)
    }
    return render(request, 'school/foreign-student.html', context)


@login_required(login_url='admin-login')
@school_required
def president_student_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        student = Student.objects.filter(status=1, school=request.user.school)
    else:
        student = Student.objects.filter(status=1, school=request.user.school, full_name__icontains=search)
    context = {
        'student': PagenatorPage(student, 50, request)
    }
    return render(request, 'school/president-school-student.html', context)


@login_required(login_url='admin-login')
@school_required
def change_teacher_view(request, pk):
    if request.method == "POST":
        full_name = request.POST['full_name']
        birth_date = request.POST.get('birth_date')
        start_study_year = request.POST['start_study_year']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')
        subject = request.POST['subject']
        st = Student.objects.get(id=pk)
        st.full_name = full_name
        st.start_study_year = start_study_year
        st.phone = phone
        st.address = address
        st.subject = Subject.objects.get(id=subject)
        if birth_date:
            st.birth_date = birth_date
        if len(request.FILES) > 0:
            st.image = image
        st.save()
    return redirect('student-profile', pk)


@login_required(login_url='admin-login')
@school_required
def add_teachers_view(request):
    context = {
        "subject": Subject.objects.all(),
    }
    return render(request, 'school/add-teacher.html', context)


@login_required(login_url='admin-login')
@school_required
def create_teacher(request):
    user = request.user
    if request.method == "POST":
        full_name = request.POST['full_name']
        birth_date = request.POST.get('birth_date')
        start_study_year = request.POST['start_study_year']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')
        subject = request.POST['subject']
        status = int(request.POST['status'])
        Student.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            start_study_year=start_study_year,
            phone=phone,
            address=address,
            image=image,
            subject_id=subject,
            status=status,
            school=user.school
        )
    return redirect('add-teacher')


@login_required(login_url='admin-login')
@school_required
def settings_view(request):
    context = {
        'city': City.objects.all()
    }
    return render(request, 'school/settings.html', context)


@login_required(login_url='admin-login')
@school_required
def change_school_view(request, pk):
    if request.method == 'POST':
        name = request.POST['name']
        director = request.POST.get('director')
        address = request.POST.get('address')
        city_id = request.POST.get('city')
        website = request.POST.get('website')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        telegram = request.POST.get('telegram')
        city = City.objects.get(id=city_id)
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        school = School.objects.get(id=pk)
        school.name = name
        school.director = director
        school.address = address
        school.city = city
        school.website = website
        school.facebook = facebook
        school.instagram = instagram
        school.telegram = telegram
        school.lat = lat
        school.lng = lng
        school.save()
        return redirect('settings')


@login_required(login_url='admin-login')
@school_required
def change_student_password(request, pk):
    if request.method == "POST":
        password = request.POST.get('password')
        st = Student.objects.get(id=pk)
        st.password = make_password(password)
        st.save()
        page = request.POST.get('page')
        if int(page) == 1:
            return redirect("president-student")
        elif int(page) == 2:
            return redirect('abuturient')
        elif int(page) == 3:
            return redirect('foreign-student')
        elif int(page) == 4:
            return redirect('teachers')
        else:
            return redirect('school-dashboard')


