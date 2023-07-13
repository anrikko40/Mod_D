from django import template


register = template.Library()


@register.filter()
def tsenzor(value):
    bad_words = ['cat', 'dog', 'opinion']
    for i in bad_words:
        value = value.replace(str(i), i[0] + '*' * (len(i) - 1))
    return value