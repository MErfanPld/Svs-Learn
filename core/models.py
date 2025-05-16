from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=255,verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255,verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('درخواست ارتباط')
        verbose_name_plural = _('درخواست‌های ارتباط')
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
