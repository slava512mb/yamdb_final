from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, ReviewCommentViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='ReviewsList',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    ReviewCommentViewSet, basename='ReviewsCommentList',
)
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('v1/', include('users.urls')),
]
