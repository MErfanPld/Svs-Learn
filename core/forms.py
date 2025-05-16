from django import forms
from .models import ContactMessage
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('نام و نام خانوادگی خود را وارد کنید'),
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('example@domain.com'),
                'required': 'required'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('موضوع خود را وارد کنید'),
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('توضیحات کامل درباره پروژه خود را بنویسید'),
                'required': 'required'
            })
        }
        labels = {
            'name': _('نام و نام خانوادگی'),
            'email': _('آدرس ایمیل'),
            'subject': _('موضوع'),
            'message': _('توضیحات'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن ستاره به لیبل فیلدهای اجباری
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label}*"
