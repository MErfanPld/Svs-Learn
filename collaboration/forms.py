from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CollaborationRequest

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ['name', 'email', 'project_type', 'details', 'budget', 'contact_method']
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
            'project_type': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('توضیحات کامل درباره پروژه خود را بنویسید'),
                'required': 'required'
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('مثال: 10-15 میلیون تومان')
            }),
            'contact_method': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }
        labels = {
            'name': _('نام و نام خانوادگی'),
            'email': _('آدرس ایمیل'),
            'project_type': _('نوع پروژه'),
            'details': _('جزئیات پروژه'),
            'budget': _('بودجه پیشنهادی (اختیاری)'),
            'contact_method': _('روش ترجیحی ارتباط'),
        }
        help_texts = {
            'budget': _('میزان بودجه خود را به تومان یا دلار مشخص کنید'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن ستاره به لیبل فیلدهای اجباری
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label}*"