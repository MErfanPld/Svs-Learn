from django import forms
from .models import Checkout 

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'phone', 'email']
        labels = {
            'full_name': 'نام کامل',
            'phone': 'شماره تماس (ترجیحا واتساپ)',
            'email': 'ایمیل',
        }
