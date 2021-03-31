from django import template

register = template.Library()


@register.inclusion_tag('messages/notification.html')
def notification(notification_type, text):
    return {
        'notification_type': notification_type,
        'text': text
    }


@register.inclusion_tag('map/rating_select.html')
def rating_select(point):
    return {
        'point': point
    }
