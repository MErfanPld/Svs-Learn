from django.db import models

# Create your models here.

from django.utils.translation import gettext_lazy as _

class CollaborationRequest(models.Model):
    class ProjectTypes(models.TextChoices):
        WEB = 'web', _('توسعه وب')
        MOBILE = 'mobile', _('توسعه موبایل')
        AI = 'ai', _('هوش مصنوعی')
        DESIGN = 'design', _('طراحی UI/UX')
        OTHER = 'other', _('سایر')

    class ContactMethods(models.TextChoices):
        EMAIL = 'email', _('ایمیل')
        PHONE = 'phone', _('تماس تلفنی')
        WHATSAPP = 'whatsapp', _('واتساپ')
        TELEGRAM = 'telegram', _('تلگرام')

    name = models.CharField(_('نام کامل'), max_length=100)
    email = models.EmailField(_('آدرس ایمیل'))
    project_type = models.CharField(
        _('نوع پروژه'), 
        max_length=50, 
        choices=ProjectTypes.choices
    )
    details = models.TextField(_('جزئیات پروژه'))
    budget = models.CharField(
        _('بودجه پیش‌نهادی'), 
        max_length=50, 
        blank=True,
        help_text=_('مثلاً 10-15 میلیون تومان یا دلاری')
    )
    contact_method = models.CharField(
        _('روش ترجیحی ارتباط'), 
        max_length=50, 
        choices=ContactMethods.choices
    )
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('درخواست همکاری')
        verbose_name_plural = _('درخواست‌های همکاری')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_project_type_display()}"