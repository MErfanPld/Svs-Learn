from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .managers import UserManager
from .validator import mobile_regex, mobile_validator
from extenstions.utils import jalali_converter
import time


def upload_image(instance, filename):
    path = 'uploads/users/' + slugify(instance.email or str(instance.phone_number), allow_unicode=True)
    name = f"{int(time.time())}-{filename}"
    return f"{path}/{name}"


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره تلفن",
        validators=[mobile_regex]
    )
    email = models.EmailField(_('ایمیل'), null=True, blank=True, unique=True)
    bio = models.TextField(_('بایو'),  null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    is_owner = models.BooleanField(_('مالک هست؟'), default=False)
    is_superuser = models.BooleanField(_('ادمین هست؟'), default=False)
    is_active = models.BooleanField(_('فعال'), default=True)
    is_staff = models.BooleanField(_('کارمند'), default=False)
    image = models.ImageField(_('تصویر'), upload_to=upload_image, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.phone_number

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email or self.phone_number or "---"

    def jcreated(self):
        return jalali_converter(self.created_at)

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = mobile_validator(str(self.phone_number)[:11])
            qs = User.objects.filter(phone_number=self.phone_number)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(_('شماره موبایل تکراری است و برای کاربر دیگری استفاده شده است!'), code="mobile")

        if self.email:
            qs = User.objects.filter(email=self.email)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(_('ایمیل تکراری است و برای کاربر دیگری استفاده شده است!'), code="email")

        super().save(*args, **kwargs)

    def get_phone(self):
        return self.phone_number

    def get_avatar(self):
        try:
            return self.image.url
        except Exception:
            return '/static/img/user-3.jpg'
