from django.urls import path

from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
