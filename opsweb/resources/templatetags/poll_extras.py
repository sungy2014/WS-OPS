from django import template

register = template.Library()

@register.filter(name="replace_to_br")
def replace_to_br(value,args):
    if args in value:
        return value.replace(args,'<br>')
    else:
        return value
