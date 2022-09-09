from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from account.models import *
from django.contrib.auth.decorators import login_required
from home.decarators import school_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib import messages


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
        'pupil_count': Student.objects.filter(status__in=[1, 2, 3], active=True, school=school).count(),
        'for_president_school_count': Student.objects.filter(status=1, active=True, school=school).count(),
        'abuturient_count': Student.objects.filter(status=2, active=True, school=school).count(),
        'foreigners_count': Student.objects.filter(status=3, active=True, school=school).count(),
        'teacher_count': Student.objects.filter(status=4, active=True, school=school).count(),
        'passive_count': Student.objects.filter(active=False, school=school).count(),
    }
    return render(request, 'school/index.html', context)


@login_required(login_url='admin-login')
@school_required
def student_profile(request, pk):
    context = {
        'teacher': Student.objects.get(id=pk),
    }
    return render(request, 'school/student-profile.html', context)


@login_required(login_url='admin-login')
@school_required
def teachers_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        teacher = Student.objects.filter(status=4, active=True, school=request.user.school)
    else:
        teacher = Student.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search), status=4, active=True, school=request.user.school)
    context = {
        'teachers': PagenatorPage(teacher, 50, request)
    }
    return render(request, 'school/teachers.html', context)


@login_required(login_url='admin-login')
@school_required
def abuturient_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        abuturient = Student.objects.filter(status=2, active=True, school=request.user.school)
    else:
        abuturient = Student.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search), status=2, active=True, school=request.user.school)
    context = {
        'abuturient': PagenatorPage(abuturient, 50, request)
    }
    return render(request, 'school/abuturient.html', context)


@login_required(login_url='admin-login')
@school_required
def foreign_student_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        student = Student.objects.filter(status=3, active=True, school=request.user.school)
    else:
        student = Student.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search), status=3, active=True, school=request.user.school)
    context = {
        'student': PagenatorPage(student, 50, request)
    }
    return render(request, 'school/foreign-student.html', context)


@login_required(login_url='admin-login')
@school_required
def president_student_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        student = Student.objects.filter(status=1, active=True, school=request.user.school)
    else:
        student = Student.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search), status=1, active=True, school=request.user.school)
    context = {
        'student': PagenatorPage(student, 50, request)
    }
    return render(request, 'school/president-school-student.html', context)


@login_required(login_url='admin-login')
@school_required
def deleted_students_view(request):
    search = request.GET.get('search')
    if search == "" or search is None:
        student = Student.objects.filter(active=False, school=request.user.school)
    else:
        student = Student.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search),
                                         active=False, school=request.user.school)
    context = {
        'student': PagenatorPage(student, 50, request)
    }
    return render(request, 'school/deleted-students.html', context)


@login_required(login_url='admin-login')
@school_required
def change_student_view(request, pk):
    if request.method == "POST":
        username = request.POST['username']
        full_name = request.POST['full_name']
        birth_date = request.POST.get('birth_date')
        start_study_year = request.POST['start_study_year']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')
        active = request.POST['active']
        status = request.POST['status']
        st = Student.objects.get(id=pk)
        st.full_name = full_name
        st.start_study_year = start_study_year
        st.phone = phone
        if username != st.username:
            if Student.objects.filter(username=username).count() > 0:
                messages.warning(request, "Bunday Foydalanuvchi mavjud usernameni o'zgartiring!")
                return redirect('student-profile', pk)
        st.username = username
        st.address = address
        st.active = int(active)
        st.status = int(status)
        if birth_date:
            st.birth_date = birth_date
        if len(request.FILES) > 0:
            st.image = image
        st.save()
        messages.success(request, "Muvofaqiyatli o'zgartirildi")
    return redirect('student-profile', pk)


@login_required(login_url='admin-login')
@school_required
def add_student_view(request):
    context = {
    }
    return render(request, 'school/add-student.html', context)


@login_required(login_url='admin-login')
@school_required
def create_student(request):
    user = request.user
    if request.method == "POST":
        full_name = request.POST['full_name']
        birth_date = request.POST.get('birth_date')
        start_study_year = request.POST['start_study_year']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')
        status = int(request.POST['status'])
        Student.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            start_study_year=start_study_year,
            phone=phone,
            address=address,
            image=image,
            status=status,
            school=user.school
        )
        messages.success(request, "Muvofaqiyatli qo'shildi")
    return redirect('add-student')


@login_required(login_url='admin-login')
@school_required
def settings_view(request):
    context = {
        'city': City.objects.all()
    }
    return render(request, 'school/settings.html', context)


@login_required(login_url='admin-login')
@school_required
def account_view(request):
    print(request.user)
    context = {
        'user': request.user
    }
    return render(request, 'school/account.html', context)


from home.viewset.auth_view import login

@login_required(login_url='admin-login')
@school_required
def change_profile_view(request, pk):
    if request.method == "POST":
        user = request.user
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username != user.username:
            if Account.objects.filter(username=username).count() > 0:
                messages.error(request, "Bunday Foydalanuvchi mavjud usernameni o'zgartiring!")
                return redirect('account')
        if len(password) < 8:
            messages.error(request, "Parol 8 ta belgidan iborat bo'lishi kerak!")
            return redirect("account")
        user.username = username
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('school-dashboard')


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


@login_required(login_url='admin-login')
@school_required
def delete_student_view(request, pk):
    st = Student.objects.get(id=pk)
    st.active = False
    st.save()
    if int(st.status) == 1:
        return redirect("president-student")
    elif int(st.status) == 2:
        return redirect('abuturient')
    elif int(st.status) == 3:
        return redirect('foreign-student')
    elif int(st.status) == 4:
        return redirect('teachers')
    else:
        return redirect('school-dashboard')

