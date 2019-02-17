from rest_framework import pagination

class CustomPagination(pagination.LimitOffsetPagination):
	default_limit = 10
	max_limit = 50
	offset_query_param = 'page'