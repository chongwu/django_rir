from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


def get_model_change_url(model):
    return reverse(
        'admin:{}_{}_change'.format(model._meta.app_label, model._meta.model_name),
        args=(model.pk,)
    )


def get_model_change_link(model):
    return "<a href={}>{}</a>".format(get_model_change_url(model), str(model))


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)
