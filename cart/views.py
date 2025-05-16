from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import *

from cart.forms import CheckoutForm
from .models import Cart, CartItem
from courses.models import Course


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        form = CheckoutForm()
        return render(request, 'cart/cart_detail.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
            return redirect('cart:success_cart')
        return render(request, 'cart/cart_detail.html', {'cart': cart, 'form': form})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, course=course)
        if not created:
            item.quantity += 1
            item.save()
        return redirect('cart:cart_detail')

    def get(self, request, course_id):
        return self.post(request, course_id)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return redirect('cart:cart_detail')

    def get(self, request, item_id):
        return self.post(request, item_id)


class SuccessCartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/success_cart.html'
