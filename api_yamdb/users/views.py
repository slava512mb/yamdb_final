from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .functions import (create_access_token, create_confirmation_code,
                        send_signup_mail)
from .models import User
from .serializers import AuthSerializer, SignUpSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = data.get('username')
    email = data.get('email')

    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = create_confirmation_code()
    user.confirmation_code = confirmation_code
    user.save()
    send_signup_mail(user)

    serializer = SignUpSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def auth(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = data.get('username')
    confirmation_code = data.get('confirmation_code')

    user = get_object_or_404(
        User, username=username)

    if not user.confirmation_code == confirmation_code:
        data = {'error': 'wrong confirmation code'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    user.confirmation_code = ''
    user.save()
    token = create_access_token(user)
    return Response(token)
