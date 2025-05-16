from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CategoryCourse, Course, Video, Enrollment

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
    fields = ('title', 'video_file', 'duration', 'order', 'is_free')
    ordering = ('order',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'course_type', 'price', 'is_active')
    list_filter = ('course_type', 'category', 'is_active', 'instructor')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('instructor', 'category')
    inlines = [VideoInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'instructor', 'category', 'course_type')
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
            'fields': ('is_active','views')
        }),
    )

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration', 'order', 'is_free')
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

admin.site.register(CategoryCourse, CategoryCourseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)

admin.site.site_header = 'مدیریت سایت فروش دوره‌های آموزشی'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'مدیریت محتوا'