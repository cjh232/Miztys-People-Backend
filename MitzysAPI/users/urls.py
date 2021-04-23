from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', UserListView.as_view()),
    path('register', UserCreate.as_view()),
    path('resend-activation', ResendActivationEmail.as_view(), name='resend-activation'),
    path('verify', VerfiyEmail.as_view(), name='verify_email'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokens/refresh', RefreshAccessTokenView.as_view(), name='token_refresh'),
    path('tokens/blacklist', LogoutView.as_view(), name='blacklist'),
    path('tokens/blacklist/all', LogoutAllView.as_view()),
    path('tokens', GetTokenPairView.as_view()),
]
