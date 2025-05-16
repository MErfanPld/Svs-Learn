from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    # Category URLs
    path('category/<slug:slug>/', CategoryCourseListView.as_view(), name='category_courses'),
    
    # Course URLs
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    
    # Filter URLs
    path('in-person/', CourseListView.as_view(), name='in_person_courses'),
    path('online/', CourseListView.as_view(), name='online_courses'),
    path('offline/', CourseListView.as_view(), name='offline_courses'),
    
    path('registration-conditions/', RegistrationConditionsView.as_view(), name='registration_conditions'),
]
