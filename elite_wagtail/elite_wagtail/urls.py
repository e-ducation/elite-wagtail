from django.conf import settings
from django.conf.urls import include, url, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

from auth_backends.urls import auth_urlpatterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from home import views as home_views

from .api import api_router

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    path('articles/<int:pk>/liked/', home_views.liked, name='liked'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'^api/v2/', api_router.urls),
    url(r'^select2/', include('django_select2.urls')),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]

urlpatterns += i18n_patterns(
    # These URLs will have /<language_code>/ appended to the beginning
    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'', include(wagtail_urls)),
    prefix_default_language=True
)

urlpatterns += auth_urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Wagtail API",
            default_version='v2',
            description="Test",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        url(r'^swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
