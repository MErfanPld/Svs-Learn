"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from .sitemaps import BlogSitemap, CourseSitemap,StaticViewSitemap

sitemaps = {
    'blogs': BlogSitemap,
    'courses': CourseSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('dashboard/', include('dashboard.urls',namespace='dashboard')),
    path('chat/whatsapp/', include('chat.urls')),
    path('cart/', include('cart.urls')),
    path('faq/', include('faq.urls')),
]

handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
handler403 = 'core.views.custom_403_view'
handler400 = 'core.views.custom_400_view'

if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + \
                  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)