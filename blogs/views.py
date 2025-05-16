# blog/views.py
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog, CategoryBlog
from .forms import BlogForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


# ================================== Category Views ==================================
class CategoryBlogListView(ListView):
    model = Blog
    template_name = 'blogs/category_blog.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(CategoryBlog, slug=self.kwargs['slug'])
        return Blog.objects.filter(category=self.category, is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# ================================== Blog Views ==================================

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 2

    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()

        next_post = Blog.objects.filter(
            created_at__gt=blog.created_at, is_published=True
        ).order_by('created_at').first()

        previous_post = Blog.objects.filter(
            created_at__lt=blog.created_at, is_published=True
        ).order_by('-created_at').first()

        categories = CategoryBlog.objects.annotate(
            post_count=Count('blog', filter=Q(blog__is_published=True))
        ).filter(post_count__gt=0)

        popular_blogs = Blog.objects.filter(is_published=True).order_by('-views')[:5]  
        context['next_post'] = next_post
        context['previous_post'] = previous_post
        context['categories'] = categories
        context['popular_blogs'] = popular_blogs  
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user
