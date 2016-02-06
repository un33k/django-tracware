from django.apps import apps
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(DjangoAppConfig):
    """
    Configuration entry point for the trackware app
    """
    label = name = 'trackware'
    verbose_name = _("trackware app")
