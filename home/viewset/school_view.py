from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(TemplateView, LoginRequiredMixin):
    # login_url = '/login'
    template_name = 'school/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            pass
            # if self.request.user.type == 4:
            #     pass
            # else:
            #     return redirect('logout')
        else:
            return redirect('login')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        return context
