from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, CourseViewSet, SectionViewSet, 
    LessonViewSet, EnrollmentViewSet, LessonProgressViewSet,
    AnnouncementViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', CourseViewSet, basename='course')
router.register(r'sections', SectionViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', LessonProgressViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]