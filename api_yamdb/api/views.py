from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User
from users.utils import generate_confirmation_code

from .filters import TitleFilter
from .permissions import (IsAuthorOrReadOnly, IsRoleAdmin, IsRoleModerator,
                          ReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ProfileSerializer, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          UserRegistrationSerializer, UserSerializer)

MAIL_SUBJECT = 'Your confirmation_code'
FROM_MAIL = 'staff@yamdb.ru'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsRoleAdmin,)

    @action(detail=False,
            methods=['GET', 'PATCH'],
            url_path='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username)
        if request.method == 'PATCH':
            if request.user.is_admin or request.user.is_superuser:
                serializer = UserSerializer(
                    user, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            serializer = ProfileSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data
        )
        if serializer.is_valid():
            confirmation_code = generate_confirmation_code()
            send_mail(
                MAIL_SUBJECT,
                confirmation_code,
                FROM_MAIL,
                [serializer.validated_data["email"]],
                fail_silently=False
            )
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = request.user
            token = RefreshToken.for_user(user)
            return Response({'token': str(token)}, status=HTTP_200_OK)
        return Response(serializer.errors,
                        status=HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    ordering_fields = ('year', 'name')
    permission_classes = (IsRoleAdmin | ReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitlePostSerializer


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (IsRoleAdmin | ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
