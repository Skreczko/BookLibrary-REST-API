from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
	message = 'You are already logged'

	def has_permission(self, request, view):
		return not request.user.is_authenticated

class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff