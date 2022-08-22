from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import School, City, Student, Account
from home.decarators import organ_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
@organ_required
def organ_dashboard_view(request):
    schools = School.objects.all().count()
    city = City.objects.all().count()
    students = Student.objects.all().count()
    staff = Account.objects.filter(status=3).count()
    abiturent = Student.objects.filter(status=2).count()
    chet_tili = Student.objects.filter(status=3).count()
    prez_maktab = Student.objects.filter(status=1).count()
    teachers = Student.objects.filter(status=4).count()
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
    citys = City.objects.all()
    q = request.GET.get('q')
    schools = School.objects.all()
    if q != '' and q is not None:
        schools = School.objects.filter(name__icontains=q)

    context = {
        'schools': PagenatorPage(schools, 10, request),
        'citys':citys
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
            lat = lat,
            lng = lng
        )
        if website is not None:
            school.website = website
        if facebook is not None:
            school.facebook = facebook
        if instagram is not  None:
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
        if lat and lng is not  None:
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
        account.username = username
        account.first_name = first_name
        account.last_name = last_name
        account.school = school
        account.save()
        return redirect('user-detail', account.id)
    return render(request, 'oranization/user-detail.html')


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


def user_delete_view(request, pk):
    user = Account.objects.get(pk=pk)
    school = School.objects.get(id=user.school.id)
    user.delete()
    return redirect('school-detail', school.id)