from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('resend-activation', ResendActivationEmail.as_view(), name='resend-activation'),
    path('verify', VerfiyEmail.as_view(), name='verify_email'),
    path('tokens/refresh', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='blacklist'),
    path('login', LoginView.as_view()),
    path('', UserDetailView.as_view())
]
