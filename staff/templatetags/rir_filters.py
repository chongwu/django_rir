from django import template

register = template.Library()


@register.filter(name='has_groups')
def has_groups(user, groups):
    return bool(user.groups.filter(name__in=groups.split(','))) | user.is_superuser
