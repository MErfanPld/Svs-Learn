from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CategoryCourse, Course, Video, Enrollment

# ================================== Category Views ==================================
class CategoryCourseListView(ListView):
    model = Course
    template_name = 'courses/category_courses.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(CategoryCourse, slug=self.kwargs['slug'])
        return Course.objects.filter(category=self.category, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# ================================== Course Views ==================================
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses_count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        return queryset


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views() 
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = self.object.videos.all().order_by('order')
        context['enrollments_count'] = Enrollment.objects.filter(course=self.object).count()
        return context



class RegistrationConditionsView(LoginRequiredMixin, ListView):
    template_name = 'courses/registration_conditions.html'
    model = Enrollment  # اضافه کردن این خط
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            is_approved=True
        ).select_related('course')
    
