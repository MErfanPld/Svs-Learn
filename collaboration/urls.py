from django.urls import path
from .views import CollaborationCreateView

app_name = 'collaboration'

urlpatterns = [
    path('request/', CollaborationCreateView.as_view(), name='request'),
]