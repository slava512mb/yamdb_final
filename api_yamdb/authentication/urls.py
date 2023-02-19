from authentication.views import get_or_create_user, get_token
from django.urls import include, path

app_name = 'authentication'

urlpatterns = [
    path('v1/auth/', include(
        [
            path('signup/', get_or_create_user, name='get_or_create_user'),
            path('token/', get_token, name='get_token'),
        ]
    )),
]
