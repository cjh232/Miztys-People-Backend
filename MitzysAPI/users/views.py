from django.shortcuts import render
from rest_framework import status, generics, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from .models import User, FailedLoginAttempt
from .utils import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from .token_utils import *


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)

        if reg_serializer.is_valid():
            new_user = reg_serializer.save()

            # Create refresh token for account activation
            AccountVerificationUtil.send_activation_email(new_user, request)

            if new_user:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendActivationEmail(APIView):

    """
    This view will send a new account activation email
    in the event that the first is never received.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        email = data['email']
        unactivated_account_set = User.objects.filter(email=email)

        if unactivated_account_set.exists():
            unactivated_account = unactivated_account_set[0]

            AccountVerificationUtil.send_activation_email(unactivated_account, request)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'There is no account using this email.'}, status=status.HTTP_404_NOT_FOUND)

class VerfiyEmail(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')

        unactivated_account = User.objects.get(id=user_id)

        if unactivated_account:
            res = AccountVerificationUtil.validate_activation_token(unactivated_account, token)
            if res:
                unactivated_account.is_active = True
                unactivated_account.save()
                return Response(
                    {
                        'msg': 'Account successfully activated!',
                        'error': False
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {
                        'msg': 'This activation link has expired or is invalid. Request a new one',
                        'error': True
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                    {
                        'msg': 'User_id/token mismatch. Request a new link.',
                        'error': True
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

class LogoutView(APIView):

    permission_classes = [AllowAny]

    """
    This view deletes the refresh_token that is
    stored in the HTTPOnly Cookie. Client will not 
    be able to refresh access token. Will need
    to re-authenticate.
    """

    def post(self, request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.status = status.HTTP_200_OK
        return response

class RefreshTokenView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token is None:
            raise exceptions.AuthenticationFailed('Refresh Token was not provided.')

        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired refresh token. Request new pair.')
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Invalid refresh token. Request a valid token pair.')

        user = User.objects.filter(id=payload.get('user_id')).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is not active.')

        if user.is_locked:
            raise exceptions.AuthenticationFailed('User is locked.')

        access_token = generate_access_token(user)

        response = Response()
        response.data = {
            'access_token': access_token
        }

        response.status = status.HTTP_200_OK

        return response

class LoginView(APIView):

    """
    Given a valid `email` and `password` pair in the 
    request JSON body, this view should return a response
    containing a new access_token. In addition to this, 
    a refresh_token will be created and stored in the 
    HTTPOnly Cookies. This helps ensure only the server
    will be able to see and use the refresh_token.
    """

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        email = request.data["email"]
        password = request.data["password"]

        if (email is None) or (password is None):
            response_data = {
                "msg": "Email and password is required.",
                "error": True
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        if user.is_locked:
            raise exceptions.AuthenticationFailed('Account is locked.')
        
        if not user.check_password(password):

            five_minutes_ago = timezone.now() + timezone.timedelta(minutes=-5)
            failed_attempt = FailedLoginAttempt(attempted_owner=user)
            failed_attempt.save()

            attempts_last_five_minutes = len(FailedLoginAttempt.objects.filter(attempted_owner=user, attempted_at__gte=five_minutes_ago))
            attempts_exceed_limit = attempts_last_five_minutes >= 5

            print(attempts_exceed_limit)

            if attempts_exceed_limit:
                user.is_locked = True
                user.save()
                raise exceptions.AuthenticationFailed('Account is locked.')

            raise exceptions.AuthenticationFailed('Bad credentials')

        serialized_user = UserSerializer(user).data

        response = Response()

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True
        )

        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response