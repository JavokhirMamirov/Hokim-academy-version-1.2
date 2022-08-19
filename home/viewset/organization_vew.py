from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import School, City
from home.decarators import organ_required


@login_required(login_url='admin-login')
@organ_required
def organ_dashboard_view(request):
    return render(request, 'oranization/index.html')

def schools_list_view(request):
    schools = School.objects.all()
    citys = City.objects.all()
    context = {
        'schools':schools,
        'citys':citys
    }
    return render(request, 'oranization/schools.html', context)


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
        website = request.POST['website']
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        telegram = request.POST['telegram']
        city = City.objects.get(id=city_id)
        school = School.objects.create(
            name=name,
            director=director,
            address=address,
            city=city,
            website=website,
            facebook=facebook,
            instagram=instagram,
            telegram=telegram
        )

    return render(request, 'oranization/add-school.html', context)

def school_detail_view (request, pk) :
    school = School.objects.get(pk=pk)
    context = {
        'school': school
    }
    return render(request, 'oranization/school-detail.html', context)

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
        return redirect('school-detail', school.id)
    context = {
        'school': school,
        'citys': citys
    }
    return render(request, 'oranization/update-school.html', context)

def school_delete_view(request, pk):
    school = School.objects.get(id=pk)
    school.delete()
    return redirect('schools')