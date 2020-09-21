from django import template

register = template.Library()


@register.simple_tag
def check_radio_value(row, value):
    return 'checked' if row.competence_val == value else ''
