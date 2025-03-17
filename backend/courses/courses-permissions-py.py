from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.user_type in ['instructor', 'admin']
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow instructor who owns the course
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user
        
        # For sections and lessons, check course instructor
        if hasattr(obj, 'course'):
            return obj.course.instructor == request.user
        
        if hasattr(obj, 'section'):
            return obj.section.course.instructor == request.user
        
        return False

class IsEnrolledOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Get course from different object types
        course = None
        if hasattr(obj, 'course'):
            course = obj.course
        elif hasattr(obj, 'section'):
            course = obj.section.course
        elif hasattr(obj, 'lesson'):
            course = obj.lesson.section.course
        
        if not course:
            return False
        
        # Check if user is instructor of the course
        if course.instructor == user:
            return True
        
        # Check if user is enrolled in the course
        return user.enrollments.filter(course=course, status='active').exists()

class IsInstructorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type in ['instructor', 'admin']
