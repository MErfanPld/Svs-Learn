from django.db import models
from django.urls import reverse
from courses.helpers import upload_courses_category_image
from extenstions.utils import jalali_converter
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField  
from multiselectfield import MultiSelectField


class CategoryCourse(models.Model):
    name = models.CharField(_('نام دسته‌بندی'), max_length=100)
    slug = models.SlugField(_('اسلاگ'), unique=True)
    image = models.ImageField(
        _('تصویر دسته بندی'), 
        upload_to='courses/', null=True,blank=True
    )
    
    class Meta:
        verbose_name = _('دسته‌بندی دوره')
        verbose_name_plural = _('دسته‌بندی دوره‌ها')
    
    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_TYPES = (
        ('in_person', _('حضوری')),
        ('online', _('آنلاین')),
        ('offline', _('آفلاین (ویدیویی)')),
    )
    
    LEVEL_TYPES = (
        ('preliminary', _('مقدماتی')),
        ('advanced', _('پیشرفته')),
        ('zero_to_one_hundred', _('صفر تا صد')),
    )
    
    title = models.CharField(_('عنوان دوره'), max_length=200)
    slug = models.SlugField(_('اسلاگ'), unique=True)
    description = RichTextField(_('توضیحات دوره'))
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name=_('مدرس')
    )
    category = models.ForeignKey(
        CategoryCourse,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('دسته‌بندی'),
        related_name='courses'
    )
    course_type = models.CharField(
        _('نوع دوره'), 
        max_length=20, 
        choices=COURSE_TYPES
    )
    course_level = models.CharField(
        _('سطح دوره'), 
        max_length=20, 
        blank=True,
        null=True,
        choices=LEVEL_TYPES
    )
    price = models.CharField(
        _('قیمت'), 
        max_length=20, 
    )
    duration = models.CharField(
        _('مدت زمان دوره'), 
        max_length=100
    )
    image = models.ImageField(
        _('تصویر دوره'), 
        upload_to='courses/'
    )
    created_at = models.DateTimeField(
        _('تاریخ ایجاد'), 
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('تاریخ آخرین ویرایش'), 
        auto_now=True
    )
    is_active = models.BooleanField(
        _('فعال'), 
        default=True
    )
    
    meeting_link = models.URLField(
        _('لینک جلسات آنلاین'), 
        blank=True, 
        null=True
    )
    schedule = models.TextField(
        _('زمان‌بندی دوره'), 
        blank=True, 
        null=True
    )
    
    total_videos = models.IntegerField(
        _('تعداد ویدیوها'), 
        default=0
    )
    total_downloads = models.IntegerField(
        _('تعداد دانلودها'), 
        default=0
    )
    
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    participant = models.PositiveIntegerField(default=0, blank=True,null=True,verbose_name="تعداد دانشجویان دوره")
    
    class Meta:
        verbose_name = _('دوره')
        verbose_name_plural = _('دوره‌ها')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def jcreated_at(self):
        return jalali_converter(self.created_at)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        
    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    def get_course_level_display(self):
        if self.course_level:
            return dict(self.LEVEL_TYPES).get(self.course_level, 'نامشخص')
        return "پایه"

class Video(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name=_('دوره مربوطه')
    )
    title = models.CharField(
        _('عنوان ویدیو'), 
        max_length=200
    )
    # video_file = models.FileField(
    #     _('فایل ویدیو'), 
    #     upload_to='videos/'
    # )
    # duration = models.DurationField(
    #     _('مدت زمان ویدیو')
    # )
    order = models.PositiveIntegerField(
        _('ترتیب نمایش'), 
        default=0
    )
    is_free = models.BooleanField(
        _('رایگان'), 
        default=False
    )
    
    class Meta:
        verbose_name = _('ویدیو')
        verbose_name_plural = _('ویدیوها')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('دانشجو')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('دوره')
    )
    enrolled_at = models.DateTimeField(
        _('تاریخ ثبت‌نام'), 
        auto_now_add=True
    )
    completed = models.BooleanField(
        _('تکمیل شده'), 
        default=False
    )
    is_approved = models.BooleanField(  
        _('تایید شده توسط ادمین'),
        default=False,
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = _('ثبت‌نام')
        verbose_name_plural = _('ثبت‌نام‌ها')
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course.title}"



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name=_('کاربر'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='comments', verbose_name=_('دوره'))
    content = models.TextField(_('متن کامنت'))
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ ویرایش'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنت‌ها')

    def __str__(self):
        return f'کامنت توسط {self.user} برای {self.course}'

    def jcreated_at(self):
        return jalali_converter(self.created_at)