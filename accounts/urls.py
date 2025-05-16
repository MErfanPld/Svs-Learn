from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
]
