from django import forms
from .models import CategoryCourse, Course, Video, Enrollment, Comment
from django.contrib.auth.models import User

class CategoryCourseForm(forms.ModelForm):
    class Meta:
        model = CategoryCourse
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'description', 'instructor', 'category',
            'course_type', 'price', 'duration', 'image', 'is_active',
            'meeting_link', 'schedule', 'total_videos', 'total_downloads'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'schedule': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_videos': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_downloads': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['course', 'title', 'video_file', 'duration', 'order', 'is_free']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'completed']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }