from django.contrib import admin
from .models import (
    Category, Course, Section, Lesson, 
    Enrollment, LessonProgress, Announcement, Review
)

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'description', 'instructor__email')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'lesson_type', 'order', 'duration')
    list_filter = ('lesson_type', 'section__course')
    search_fields = ('title', 'description', 'section__title', 'section__course__title')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'progress', 'enrolled_at', 'completed_at')
    list_filter = ('status', 'enrolled_at')
    search_fields = ('user__email', 'course__title')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'course__title', 'comment')

admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(LessonProgress)
admin.site.register(Announcement)
admin.site.register(Review, ReviewAdmin)
