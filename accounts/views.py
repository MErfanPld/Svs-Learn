from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from .forms import SignUpForm, LoginForm


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('core:home') 


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')
