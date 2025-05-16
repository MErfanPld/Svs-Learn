from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("رمز عبور با تأیید رمز عبور مطابقت ندارد.")
        
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="شماره تلفن")
    password = forms.CharField(widget=forms.PasswordInput)
