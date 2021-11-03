from django import template


register = template.Library()

# create custom template tags and filters in django documentation
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
