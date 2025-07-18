from django.shortcuts import get_object_or_404, redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.db.models import Count, Q

from courses.forms import CommentForm
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


class CourseDetailView(FormMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    form_class = CommentForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['videos'] = course.videos.all().order_by('order')
        context['enrollments_count'] = Enrollment.objects.filter(course=course).count()
        context['comments'] = course.comments.all()
        context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login') 

        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.course = self.object
            comment.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class RegistrationConditionsView(LoginRequiredMixin, ListView):
    template_name = 'courses/registration_conditions.html'
    model = Enrollment  
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            is_approved=True
        ).select_related('course')
    

class CourseTypeListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        course_type = self.kwargs.get('course_type')
        category_ids = self.request.GET.getlist('category')
        search_query = self.request.GET.get('search', '')

        queryset = Course.objects.filter(course_type=course_type, is_active=True)

        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        sort = self.request.GET.get('sort')
        if sort == 'popular':
            queryset = queryset.order_by('-views')
        elif sort == 'new':
            queryset = queryset.order_by('-created_at')
        elif sort == 'special':
            queryset = queryset.filter(is_special=True)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['selected_categories'] = self.request.GET.getlist('category')
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_type'] = self.kwargs.get('course_type')

        categories = CategoryCourse.objects.annotate(
            count=Count('courses', filter=Q(courses__is_active=True, courses__course_type=self.kwargs.get('course_type')))
        )

        context['categories'] = categories

        return context