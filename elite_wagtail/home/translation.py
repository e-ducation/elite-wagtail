from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import HomePage, ArticlePage, ArticleListPage, Advert


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'body',
    )

@register(Advert)
class AdvertTR(TranslationOptions):
    fields = (
        "title",
        "raw_html",
    )

@register(ArticlePage)
class ArticlePageTR(TranslationOptions):
    pass

@register(ArticleListPage)
class ArticleListPageTR(TranslationOptions):
    pass
