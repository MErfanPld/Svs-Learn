from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView, SuccessCartView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:course_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('success/', SuccessCartView.as_view(), name='success_cart'),
]
