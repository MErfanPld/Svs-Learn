from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Faq(models.Model):
    title = models.CharField(_('عنوان سوال'), max_length=100)
    body = models.TextField(_('متن'))
    
    class Meta:
        verbose_name = _('سوالات متداول')
        verbose_name_plural = _('سوالات متداول‌ها')
    
    def __str__(self):
        return self.title