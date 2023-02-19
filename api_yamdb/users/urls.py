from django.urls import path

from .views import auth, signup

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', auth, name='auth')
]
