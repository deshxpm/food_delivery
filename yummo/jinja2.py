from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime as django_naturaltime
from django.conf import settings
from django.apps import apps
from django_middleware_global_request.middleware import get_request


def get_base_url():
    try:
        request = get_request()
        return request.META['HTTP_HOST']
    except Exception as e:
        print(e)
        return settings.BASE_URL


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_base_url':get_base_url,
        'filter': getter_multiple_obj,

    })    

    return env

def getter_multiple_obj(app_name, model_name, **kwargs):
    """function to get the single model object based on the filter"""
    __class = apps.get_model(app_label=app_name, model_name=model_name)
    return __class.objects.filter(**kwargs)

