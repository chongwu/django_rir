from django.urls import reverse


def get_model_change_url(model):
    return reverse(
        'admin:{}_{}_change'.format(model._meta.app_label, model._meta.model_name),
        args=(model.pk,)
    )


def get_model_change_link(model):
    return "<a href={}>{}</a>".format(get_model_change_url(model), str(model))
