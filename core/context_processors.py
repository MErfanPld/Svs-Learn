from blogs.models import CategoryBlog
from courses.models import CategoryCourse

def categories_context(request):
    categories = CategoryCourse.objects.all()
    return {'navbar_categories': categories}

def categories_blog_context(request):
    categories = CategoryBlog.objects.all()
    return {'navbar_blog_categories': categories}
