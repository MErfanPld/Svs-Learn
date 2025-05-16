from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.RoadmapView.as_view(), name='roadmap'),
]
