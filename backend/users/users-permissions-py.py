from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow admin users
        if request.user.user_type == 'admin':
            return True
            
        # Allow owner
        return obj.id == request.user.id
