from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banking'
    label = 'banking'
    verbose_name = _('API banking')
    default = False
