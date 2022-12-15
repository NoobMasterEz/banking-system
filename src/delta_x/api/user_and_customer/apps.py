from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delta_x'
    label = 'delta_x'
    verbose_name = _('API delta_x')
    default = False
