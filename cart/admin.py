from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('course', 'quantity')
    can_delete = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at','total_price')
    list_filter = ('created_at',)
    search_fields = ('user__phone_number', 'user__email')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'course', 'quantity')
    search_fields = ('course__title', 'cart__user__phone_number')


from .models import Checkout

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'created_at')
    search_fields = ('full_name', 'phone', 'email')