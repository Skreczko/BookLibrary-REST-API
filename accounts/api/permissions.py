from rest_framework import permissions

METHODS = ('GET', 'OPTIONS', 'HEAD')

class IsAnonymous(permissions.BasePermission):
	message = 'You are already logged'
	def has_permission(self, request, view):
		return not request.user.is_authenticated


class IsStaffUser(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.is_staff


class IsStaffOrOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(request.user.is_staff or obj.user==request.user)


class IsStaffObjectPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(
				request.method in METHODS and request.user.is_authenticated or
				request.user.is_staff
			)


class IsStaffCRUDPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.method in METHODS and request.user.is_authenticated or
				request.user.is_staff
			)


class IsStaffOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		return bool(
			request.method in METHODS or
			request.user and
			request.user.is_staff
		)