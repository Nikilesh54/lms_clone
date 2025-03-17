from rest_framework import serializers
from .models import (
    Category, Course, Section, Lesson, 
    Enrollment, LessonProgress, Announcement, Review
)
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'course', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'enrollment', 'lesson', 'is_completed',
            'watched_duration', 'last_position', 'viewed_at'
        ]
        read_only_fields = ['viewed_at']Serializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'section', 'title', 'description', 'lesson_type',
            'content', 'video_url', 'video_file', 'pdf_file', 
            'quiz', 'order', 'duration'
        ]

class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = ['id', 'course', 'title', 'description', 'order', 'lessons']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'course', 'title', 'content', 'created_at']
        read_only_fields = ['created_at']

class CourseListSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'category',
            'instructor', 'thumbnail', 'price', 'is_published',
            'created_at', 'updated_at', 'enrollment_count', 'average_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    announcements = AnnouncementSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'category',
            'instructor', 'thumbnail', 'price', 'is_published',
            'created_at', 'updated_at', 'sections', 'announcements',
            'reviews', 'enrollment_count', 'average_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'enrolled_at',
            'completed_at', 'status', 'progress'
        ]
        read_only_fields = ['enrolled_at', 'completed_at']

class Lesson