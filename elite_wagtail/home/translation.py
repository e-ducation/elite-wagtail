from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import HomePage, ArticlePage, ArticleListPage


@register(HomePage)
class HomePageTR(TranslationOptions):
   pass


@register(ArticlePage)
class ArticlePageTR(TranslationOptions):
    fields = (
        'author_name',
    )

@register(ArticleListPage)
class ArticleListPageTR(TranslationOptions):
    pass
