from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blogs.models import Blog
from courses.models import Course

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Course.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'core:about_us',      
            'core:contact_us',
            'roadmap:roadmap',
            'collaboration:request',
        ]

    def location(self, item):
        return reverse(item)
