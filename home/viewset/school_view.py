from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from account.models import *
from django.contrib.auth.decorators import login_required
from home.decarators import school_required


@login_required(login_url='admin-login')
@school_required
def dashboard(request):
    context = {
        'pupil_count': Student.objects.filter(status__in=[1, 2, 3])
    }
    return render(request, 'school/index.html', context)


@login_required(login_url='admin-login')
@school_required
def teacher_profile(request, pk):
    context = {
        'teacher': Student.objects.get(id=pk),
        'subject': Subject.objects.all()
    }
    return render(request, 'school/teacher-profile.html', context)


@login_required(login_url='admin-login')
@school_required
def teachers_view(request):
    context = {
        'teachers': Student.objects.filter(status=4)
    }
    return render(request, 'school/teachers.html', context)


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
    return redirect('teacher-profile', pk)


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
    if request.method == "POST":
        full_name = request.POST['full_name']
        birth_date = request.POST.get('birth_date')
        start_study_year = request.POST['start_study_year']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')
        subject = request.POST['subject']
        Student.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            start_study_year=start_study_year,
            phone=phone,
            address=address,
            image=image,
            subject_id=subject,
            status=4
        )
    return redirect('add-teacher')

