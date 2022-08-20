from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from home.decarators import organ_required


@login_required(login_url='admin-login')
@organ_required
def organ_dashboard_view(request):
    return render(request, 'oranization/index.html')