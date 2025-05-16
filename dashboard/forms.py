from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from users.validator import mobile_regex, mobile_validator

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
            'image': 'تصویر پروفایل',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_number = mobile_validator(str(phone_number)[:11])
            qs = User.objects.filter(phone_number=phone_number)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('شماره موبایل تکراری است و برای کاربر دیگری استفاده شده است!')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('ایمیل تکراری است و برای کاربر دیگری استفاده شده است!')
        return email