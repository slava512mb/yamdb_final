from django.urls import include, path
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       GetTokenView, ReviewViewSet, TitleViewSet,
                       UserRegistrationView, UserViewSet)
from rest_framework.routers import SimpleRouter

router_v1 = SimpleRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)' r'/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserRegistrationView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view())
]
