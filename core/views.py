import random
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView

from blogs.models import Blog
from courses.models import CategoryCourse, Course

from .forms import ContactForm


# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # دریافت پارامترهای جستجو
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')

        # فیلتر کردن دوره‌ها بر اساس جستجو
        courses = Course.objects.all()
        if search_query:
            courses = courses.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if category_id:
            courses = courses.filter(categories__id=category_id)

        # دسته‌بندی‌های پرطرفدار
        categories = (
            CategoryCourse.objects.annotate(num_courses=Count('courses'))
            .order_by('-num_courses')[:3]
        )

        context['categories'] = categories
        context['all_categories'] = CategoryCourse.objects.all()  # برای dropdown جستجو
        context['popular_courses'] = Course.objects.order_by('-views')[:4]
        context['latest_blogs'] = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]
        context['search_results'] = courses
        context['search_query'] = search_query
        context['selected_category'] = category_id
        
        return context
    

class SearchResultsView(ListView):
    template_name = 'core/search_results.html'
    context_object_name = 'courses'
    paginate_by = 10  # اختیاری - برای صفحه‌بندی نتایج

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Course.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query))
        return Course.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context    

    
class AboutUsView(TemplateView):
    template_name = 'core/about_us.html'
    
    
class ContactUsView(FormView):
    template_name = 'core/contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact_us')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد.")
        return super().form_valid(form)
    
    
def custom_404_view(request, exception):
    return render(request, "core/errors/404.html", status=404)

def custom_500_view(request):
    return render(request, "core/errors/500.html", status=500)

def custom_403_view(request, exception):
    return render(request, "core/errors/403.html", status=403)

def custom_400_view(request, exception):
    return render(request, "core/errors/400.html", status=400)