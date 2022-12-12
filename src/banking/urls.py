from django.urls import include, path, re_path
from django.conf.urls import (
    handler400,
    handler403,
    handler404,
    handler500)

from .api.utiles import schema_view
from .api.routers import router

handler403 = 'module.cores.custom_permission_denied_view'
handler404 = 'module.cores.custom_page_not_found_view'
handler500 = 'module.cores.custom_error_view'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('module/', include('banking.module.urls', namespace='module')),
    path('dashboard/', include('banking.module.dashboard.urls', namespace='dashboard')),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
