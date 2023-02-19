from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateDeleteListViewSet
from .permissions import (AdminModerAuthorOrReadOnly, AdminOrReadOnly,
                          AdminOrSuperuser)
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewCommentSerializer, ReviewSerializer,
                          TitleSerializer, TitleSerializerList, UserSerializer)
from .services import get_review_object


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        AdminModerAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (filters.OrderingFilter,)
    ordering = ['id']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        serializer.save(author=author, title=title)


class ReviewCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCommentSerializer
    permission_classes = (
        AdminModerAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ['id']

    def get_queryset(self):
        comments = get_review_object(self).comments
        return comments.all()

    def perform_create(self, serializer):
        review = get_review_object(self)
        author = self.request.user
        serializer.save(author=author, review=review)


class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ]
    search_fields = ['name']
    ordering = ['id']


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ]
    search_fields = ['name']
    ordering = ['id']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, ]
    filterset_class = TitleFilter
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializerList
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering = ['username']
    search_fields = ['username']

    @action(detail=False,
            methods=('get', 'patch'),
            url_path=r'me',
            permission_classes=(IsAuthenticated,))
    def me(self, request, format=None):
        me = self.request.user

        if request.method == 'GET':
            serializer = UserSerializer(me)
            return Response(serializer.data)

        data = self.request.data.copy()
        data.pop('role', None)
        data['email'] = me.email
        data['username'] = me.username
        serializer = UserSerializer(me, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
