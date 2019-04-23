from wagtail.api.v2.endpoints import PagesAPIEndpoint, BaseAPIEndpoint
from taggit.models import Tag
from rest_framework.pagination import PageNumberPagination
from .models import ArticlePage


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


class TagsAPIEndpoint(BaseAPIEndpoint):
    body_fields = BaseAPIEndpoint.body_fields + ['name']
    name = 'tags'
    model = Tag

    def get_queryset(self):
        return ArticlePage.tags.all()
