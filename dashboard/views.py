from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from courses.models import Enrollment
from users.models import User
from .forms import ProfileUpdateForm


# Create your views here.

class DashboardView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/dashboard.html'
    model = Enrollment
    context_object_name = 'enrollments'
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            is_approved=True
        ).select_related('course')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'dashboard/profile_update.html'
    success_url = reverse_lazy('dashboard:profile_edit')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ویرایش اکانت شما با موفقیت انجام شد.")
        return super().form_valid(form)
