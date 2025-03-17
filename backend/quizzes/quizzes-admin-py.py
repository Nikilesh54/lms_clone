from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'order')
    list_filter = ('quiz', 'question_type')
    search_fields = ('question_text', 'quiz__title')
    inlines = [ChoiceInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit', 'pass_percentage', 'max_attempts', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    readonly_fields = ('question', 'is_correct', 'points_earned')

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed', 'time_spent', 'started_at', 'completed_at')
    list_filter = ('passed', 'started_at', 'completed_at')
    search_fields = ('user__email', 'quiz__title')
    readonly_fields = ('score', 'passed', 'time_spent')
    inlines = [QuestionResponseInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionResponse)
