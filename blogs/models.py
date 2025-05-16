from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from extenstions.utils import jalali_converter

User = get_user_model()

class CategoryBlog(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(unique=True, blank=True, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "مقاله دسته‌بندی"
        verbose_name_plural = "دسته‌بندی مقاله ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="نویسنده مقاله")
    title = models.CharField(max_length=200,verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, blank=True,verbose_name="اسلاگ مقاله")
    category = models.ForeignKey(CategoryBlog, on_delete=models.SET_NULL, null=True,verbose_name="دسته بندی مقاله")
    content = models.TextField(verbose_name="محتوا")
    image = models.ImageField(upload_to='blog/', null=True, blank=True,verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ساخت")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")
    is_published = models.BooleanField(default=True,verbose_name="انتشار یافته؟")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.image.url if self.image else ''
    
    def jcreated_at(self):
        return jalali_converter(self.created_at)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        
    def get_absolute_url(self):
            return reverse('blogs:detail', kwargs={'slug': self.slug})