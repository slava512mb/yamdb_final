from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='urls')),
    path('api/', include(
        'authentication.urls',
        namespace='authentication'
    )),
    path(
        'redoc-TechSpec/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    )
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

schema_view = get_schema_view(
    openapi.Info(
        title="YAMDB API",
        default_version='v1',
        description="Документация для приложения YAMDB API",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="polikarskij@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
