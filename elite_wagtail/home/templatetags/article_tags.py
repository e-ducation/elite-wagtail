from django.template import Library
from home.models import ArticlePage, PopularArticle


register = Library()


@register.inclusion_tag('home/tags/popular_articles.html', takes_context=True)
def popular_articles(context):
    if PopularArticle.objects.all():
        pop_article = PopularArticle.objects.all().first()
        return {
            'pop_article': pop_article
        }
    else:
        return None


@register.simple_tag(takes_context=True)
def previous_article(context):
    page = context['page']
    if page.get_prev_siblings():
        prev_page = page.get_prev_siblings().first()
        return {
            'prev_url', prev_page.get_url(),
            'title', prev_page.title,
        }
    else:
        return 'no more'


@register.simple_tag(takes_context=True)
def next_article(context):
    page = context['page']
    if page.get_next_siblings():
        next_page = page.get_next_siblings().first()
        return {
            'next_url', next_page.get_url(),
            'title', next_page.title,
        }
    else:
        return 'no more'


@register.inclusion_tag('home/tags/prev_and_next_article.html', takes_context=True)
def prev_and_next_article(context):
    page = context['page']
    article = {
        'prev_url': '#',
        'prev_title': '没有了',
        'next_url': '#',
        'next_title': '没有了',
    }
    if page.get_prev_siblings():
        prev_page = page.get_prev_siblings().first()
        article['prev_url'] = prev_page.get_url()
        article['prev_title'] = prev_page.title

    if page.get_next_siblings():
        next_page = page.get_next_siblings().first()
        article['next_url'] = next_page.get_url()
        article['next_title'] = next_page.title

    return article
