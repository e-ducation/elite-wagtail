from datetime import date

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.search.models import Query


class ArticleListRoutes(RoutablePageMixin):

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def entries_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = _('tag')
        self.search_term = tag
        self.entries = self.get_entries().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        self.entries = self.get_entries()
        return Page.serve(self, request, *args, **kwargs)
