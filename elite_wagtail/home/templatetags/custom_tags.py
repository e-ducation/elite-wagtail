from django import template

from taggit.models import Tag

register = template.Library()


@register.filter(name='gen_href')
def gen_href(link):
    return '''href={} target="_blank"'''.format(link) if link else ''


@register.inclusion_tag('home/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    article_page = context['article_page']
    if tags_qs:
        tags = tags_qs.all().distinct()
    else:
        entries = article_page.get_entries()
        tags = Tag.objects.filter(articlepage__in=entries).distinct()
    if limit:
        tags = tags[:limit]

    context['tags'] = tags
    return context    
