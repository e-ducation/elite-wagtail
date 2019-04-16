from wagtail.api.v2.endpoints import PagesAPIEndpoint
from rest_framework.pagination import PageNumberPagination


class NewPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class AppPagesAPIEndpoint(PagesAPIEndpoint):
    pagination_class = NewPageNumberPagination
    known_query_parameters = PagesAPIEndpoint.known_query_parameters.union([
        'page_size',
        'page',
    ])
    meta_fields = [
        'html_url',
        'parent',
    ]