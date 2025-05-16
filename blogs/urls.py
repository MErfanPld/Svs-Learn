from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('category/<slug:slug>/', views.CategoryBlogListView.as_view(), name='category_blog'),
    # path('<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='update'),
    # path('<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('create/', views.BlogCreateView.as_view(), name='create'),
    path('', views.BlogListView.as_view(), name='list'),
]
