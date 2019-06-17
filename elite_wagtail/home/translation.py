from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import HomePage, ArticlePage, ArticleListPage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'body',
    )


@register(ArticlePage)
class ArticlePageTR(TranslationOptions):
    pass

@register(ArticleListPage)
class ArticleListPageTR(TranslationOptions):
    pass
