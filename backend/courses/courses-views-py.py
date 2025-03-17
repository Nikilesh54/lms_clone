from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from .models import (
    Category, Course, Section, Lesson, 
    Enrollment, LessonProgress, Announcement, Review
)
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer, 
    SectionSerializer, LessonSerializer, EnrollmentSerializer, 
    LessonProgressSerializer, AnnouncementSerializer, ReviewSerializer
)
from .permissions import (
    IsInstructorOrReadOnly, IsEnrolledOrInstructor, 
    IsInstructorOrAdmin
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsInstructorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsInstructorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'price']
    
    def get_queryset(self):
        queryset = Course.objects.annotate(
            enrollment_count=Count('enrollments', distinct=True),
            average_rating=Avg('reviews__rating')
        )
        
        # Filter by instructor
        instructor_id = self.request.query_params.get('instructor_id')
        if instructor_id:
            queryset = queryset.filter(instructor_id=instructor_id)
        
        # Filter by category
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(
                Q(category_id=category_id) | 
                Q(category__parent_id=category_id)
            )
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Show only published courses for non-instructors
        if not self.request.user.is_authenticated or self.request.user.user_type == 'student':
            queryset = queryset.filter(is_published=True)
        elif self.request.user.user_type == 'instructor':
            # Instructors can see all their courses and published courses from others
            queryset = queryset.filter(
                Q(instructor=self.request.user) | 
                Q(is_published=True)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        # Check if user is already enrolled
        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response(
                {'detail': 'You are already enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            user=user,
            course=course,
            status='active'
        )
        
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        # Check if user is enrolled in the course
        if not Enrollment.objects.filter(user=user, course=course).exists():
            return Response(
                {'detail': 'You must be enrolled in the course to review it.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user has already reviewed the course
        existing_review = Review.objects.filter(user=user, course=course).first()
        if existing_review:
            serializer = ReviewSerializer(existing_review, data=request.data, partial=True)
        else:
            serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=user, course=course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Section.objects.filter(course_id=course_id)
        return Section.objects.all()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        section_id = self.request.query_params.get('section_id')
        if section_id:
            return Lesson.objects.filter(section_id=section_id)
        return Lesson.objects.all()
            
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        lesson = self.get_object()
        user = request.user
        
        try:
            enrollment = Enrollment.objects.get(user=user, course=lesson.section.course)
            progress, created = LessonProgress.objects.get_or_create(
                enrollment=enrollment,
                lesson=lesson
            )
            serializer = LessonProgressSerializer(progress)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response(
                {'detail': 'You are not enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        lesson = self.get_object()
        user = request.user
        
        # Get data from request
        is_completed = request.data.get('is_completed', False)
        last_position = request.data.get('last_position', 0)
        watched_duration = request.data.get('watched_duration', 0)
        
        try:
            enrollment = Enrollment.objects.get(user=user, course=lesson.section.course)
            progress, created = LessonProgress.objects.get_or_create(
                enrollment=enrollment,
                lesson=lesson,
                defaults={
                    'is_completed': is_completed,
                    'last_position': last_position,
                    'watched_duration': watched_duration
                }
            )
            
            if not created:
                progress.is_completed = is_completed
                progress.last_position = last_position
                progress.watched_duration = watched_duration
                progress.save()
            
            # Update course progress
            self._update_course_progress(enrollment)
            
            serializer = LessonProgressSerializer(progress)
            return Response(serializer.data)
            
        except Enrollment.DoesNotExist:
            return Response(
                {'detail': 'You are not enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _update_course_progress(self, enrollment):
        """Helper method to update course progress"""
        total_lessons = Lesson.objects.filter(section__course=enrollment.course).count()
        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()
        
        enrollment.progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        
        # Check if course is completed
        if enrollment.progress >= 100:
            enrollment.status = 'completed'
            enrollment.completed_at = timezone.now()
        
        enrollment.save()
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        lesson = self.get_object()
        user = request.user
        
        try:
            enrollment = Enrollment.objects.get(user=user, course=lesson.section.course)
        except Enrollment.DoesNotExist:
            return Response(
                {'detail': 'You are not enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lesson_progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson,
            defaults={'is_completed': True, 'last_position': request.data.get('last_position', 0), 'watched_duration': request.data.get('watched_duration', 0)}
        )
        
        if not created:
            lesson_progress.is_completed = True
            lesson_progress.last_position = request.data.get('last_position', lesson_progress.last_position)
            lesson_progress.watched_duration = request.data.get('watched_duration', lesson_progress.watched_duration)
            lesson_progress.save()
        
        # Update course progress
        total_lessons = Lesson.objects.filter(section__course=lesson.section.course).count()
        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()
        
        enrollment.progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        
        # Check if course is completed
        if enrollment.progress >= 100:
            enrollment.status = 'completed'
            enrollment.completed_at = timezone.now()
        
        enrollment.save()
        
        serializer = LessonProgressSerializer(lesson_progress)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Students can see only their enrollments
        if user.user_type == 'student':
            return Enrollment.objects.filter(user=user)
        
        # Instructors can see enrollments for their courses
        elif user.user_type == 'instructor':
            return Enrollment.objects.filter(course__instructor=user)
        
        # Admins can see all enrollments
        return Enrollment.objects.all()
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        enrollments = Enrollment.objects.filter(
            user=request.user,
            status='active'
        )
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        enrollment = self.get_object()
        
        if enrollment.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollment.status = 'completed'
        enrollment.completed_at = timezone.now()
        enrollment.save()
        
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)

class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Filter by enrollment (course)
        enrollment_id = self.request.query_params.get('enrollment_id')
        if enrollment_id:
            return LessonProgress.objects.filter(enrollment_id=enrollment_id)
        
        # Students can see only their progress
        if user.user_type == 'student':
            return LessonProgress.objects.filter(enrollment__user=user)
        
        # Instructors can see progress for students in their courses
        elif user.user_type == 'instructor':
            return LessonProgress.objects.filter(enrollment__course__instructor=user)
        
        # Admins can see all progress
        return LessonProgress.objects.all()

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Announcement.objects.filter(course_id=course_id)
        return Announcement.objects.all()
    
    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        course = Course.objects.get(id=course_id)
        
        if course.instructor != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to create announcements for this course.")
        
        serializer.save()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Review.objects.filter(course_id=course_id)
        
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Review.objects.filter(user_id=user_id)
        
        return Review.objects.all()
    
    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        
        # Check if user is enrolled in the course
        if not Enrollment.objects.filter(user=self.request.user, course_id=course_id).exists():
            raise permissions.PermissionDenied("You must be enrolled in the course to review it.")
        
        # Check if user has already reviewed the course
        if Review.objects.filter(user=self.request.user, course_id=course_id).exists():
            raise permissions.PermissionDenied("You have already reviewed this course.")
        
        serializer.save(user=self.request.user)
