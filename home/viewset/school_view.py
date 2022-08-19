from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import *


class Dashboard(TemplateView):
    # login_url = '/login'
    template_name = 'school/index.html'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     pass
        #     # if self.request.user.type == 3:
        #     #     pass
        #     # else:
        #     #     return redirect('logout')
        # else:
        #     return redirect('login')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        return context


class TeacherProfile(TemplateView):
    # login_url = '/login'
    template_name = 'school/teacher-profile.html'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     pass
        #     # if self.request.user.type == 3:
        #     #     pass
        #     # else:
        #     #     return redirect('logout')
        # else:
        #     return redirect('login')
        return super(TeacherProfile, self).dispatch(*args, **kwargs)

    def get_context_data(self, pk, **kwargs):
        context = {
            'teacher': Student.objects.get(id=pk),
            'subject': Subject.objects.all()
        }
        return context


class TeachersView(TemplateView):
    # login_url = '/login'
    template_name = 'school/teachers.html'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     pass
        #     # if self.request.user.type == 3:
        #     #     pass
        #     # else:
        #     #     return redirect('logout')
        # else:
        #     return redirect('login')
        return super(TeachersView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'teachers': Student.objects.filter(status=4)
        }
        return context


def ChangeTeacher(request, pk):
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


class AddTeacher(TemplateView):
    # login_url = '/login'
    template_name = 'school/add-teacher.html'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     pass
        #     # if self.request.user.type == 3:
        #     #     pass
        #     # else:
        #     #     return redirect('logout')
        # else:
        #     return redirect('login')
        return super(AddTeacher, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "subject": Subject.objects.all(),
        }
        return context

