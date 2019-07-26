from django import template
from taggit.models import Tag
from django.contrib.admin.templatetags.admin_list import result_headers

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


@register.inclusion_tag("home/userfeeback_list.html", takes_context=True)
def userfeeback_list(context):
    """
    Displays the headers and data list together
    """
    view = context['view']
    headers = list(result_headers(view))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    context.update({
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields
        })  
    return context


@register.inclusion_tag("home/image_list.html", takes_context=True)
def image_list(context):
    """
    Displays the image list together
    """ 
    try:
        pic_url_list = str(context['items'].image_url).split(',')
    except Exception as e:
        print(e)
        pic_url_list = [] 
    context.update({
        'pic_list': pic_url_list
    })    

    return context