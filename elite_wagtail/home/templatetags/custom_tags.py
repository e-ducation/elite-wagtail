from django import template

register = template.Library()


@register.filter(name='gen_href')
def gen_href(link):
    return '''href=" {}" target="_blank"'''.format(link) if link else ''
