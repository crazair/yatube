from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def uglify(text):
    text_result = ''
    for i in range(len(text)):
        if i % 2 == 0:
            text_result += text[i].upper()
        else:
            text_result += text[i].lower()
    return text_result
