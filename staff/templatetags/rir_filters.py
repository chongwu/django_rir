from django import template
from ..models import Person

register = template.Library()


@register.filter(name='has_groups')
def has_groups(user, groups):
    return bool(user.groups.filter(name__in=groups.split(','))) | user.is_superuser


@register.simple_tag(name='is_mentor')
def is_mentor(user, person_id):
    if not user.is_anonymous:
        try:
            if person_id in user.person.students.values_list('tab_number', flat=True):
                return True
        except Person.DoesNotExist:
            pass
    return False


@register.simple_tag(name='is_chief')
def is_chief(user, person_id):
    if not user.is_anonymous:
        person = Person.objects.prefetch_related('department').get(tab_number=person_id)
        try:
            # TODO Оптимизировать условие, если возможно
            if user.person.current_department():
                if person.current_department().id == user.person.current_department().id and user.person.current_position().chief:
                    return True
        except Person.DoesNotExist:
            pass
    return False
