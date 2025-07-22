from django.contrib import admin , messages
from django.contrib.auth.admin import UserAdmin
from django.utils.text import slugify
from django.contrib.auth.models import User

from courses.helpers import generate_random_string
from .models import CategoryCourse, Course, Video, Enrollment,Comment


@admin.action(description="کپی کردن دوره‌های انتخاب‌شده")
def duplicate_courses(modeladmin, request, queryset):
    copied = 0
    for obj in queryset:
        old_slug = obj.slug
        obj.pk = None 
        obj.slug = f"{slugify(obj.title)}-{generate_random_string()}" 
        obj.save()
        copied += 1
    messages.success(request, f"{copied} دوره با موفقیت کپی شد.")

@admin.action(description="فعال‌سازی دوره‌های انتخاب‌شده")
def activate_courses(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    messages.success(request, f"{updated} دوره فعال شد.")

@admin.action(description="غیرفعال‌سازی دوره‌های انتخاب‌شده")
def deactivate_courses(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    messages.success(request, f"{updated} دوره غیرفعال شد.")

@admin.action(description="افزایش بازدید دوره‌های انتخاب‌شده ")
def increase_views(modeladmin, request, queryset):
    for course in queryset:
        course.views += 100  # یا هر مقدار دلخواه
        course.save(update_fields=['views'])
    messages.success(request, "بازدید دوره‌ها افزایش یافت.")

class CategoryCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'course_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'تعداد دوره‌ها'

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('title', 'order', 'is_free')
    ordering = ('order',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'course_type', 'course_level','price', 'is_active')
    list_filter = ('course_type', 'category', 'is_active', 'instructor')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('instructor', 'category')
    inlines = [VideoInline]
    actions = [duplicate_courses,activate_courses,deactivate_courses,increase_views] 
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'instructor', 'category', 'course_type','course_level',)
        }),
        ('اطلاعات مالی', {
            'fields': ('price',)
        }),
        ('تنظیمات زمانی', {
            'fields': ('duration', 'schedule')
        }),
        ('تنظیمات رسانه', {
            'fields': ('image', 'meeting_link', 'total_videos', 'total_downloads')
        }),
        ('تنظیمات وضعیت', {
            'fields': ('is_active','views','participant')
        }),
    )

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_free')
    list_filter = ('is_free', 'course__course_type', 'course')
    search_fields = ('title', 'course__title')
    raw_id_fields = ('course',)
    ordering = ('course', 'order')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed')
    list_filter = ('completed', 'course__course_type', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
    raw_id_fields = ('student', 'course')
    date_hierarchy = 'enrolled_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'short_content', 'jcreated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'course__title', 'content')
    readonly_fields = ('user', 'course', 'content', 'jcreated_at')

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'متن کوتاه'


admin.site.register(CategoryCourse, CategoryCourseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)

admin.site.site_header = ' SVS LEARN مدیریت سایت دوره‌های آموزشی'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'مدیریت ماژول ها'