from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
