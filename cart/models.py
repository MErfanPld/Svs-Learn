from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = ' سبد خرید'
        verbose_name_plural = ' سبد های خرید'

    def __str__(self):
        return f"سبد خرید {self.user}"

    def total_price(self):
        return sum(item.course.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        unique_together = ('cart', 'course')
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'

    def __str__(self):
        return f"{self.course.title} x {self.quantity}"

    def total_price(self):
        return self.course.price * self.quantity


class Checkout(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    email = models.EmailField(verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = 'تسویه حساب'
        verbose_name_plural = 'تسویه حساب ها'

    def __str__(self):
        return f"{self.full_name} - {self.phone}"