from django.shortcuts import render
from rest_framework import status, generics
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


class UserCreate(APIView):
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

    def get(self, request):
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

class UserListView(generics.ListAPIView):
    # permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# View to logout and blacklist the token
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            blacklist_token(refresh_token) # Blacklisting prevents unauthorized usage 
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):

    def post(self, request):
        user_id = request.user.id # User id taken from given Access Token

        tokens = OutstandingToken.objects.filter(user_id=user_id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        
        return Response(data= {'status':'Logged out from all accounts!'}, status=status.HTTP_205_RESET_CONTENT)

class GetTokenPairView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        data = request.data

        given_email = data["email"]  # Email submitted to the form on the frontend by the user
        given_pswd = data['password']  # Password submitted to the form on the frontend by the user

        try:
            requested_user = User.objects.get(email=given_email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {
                    'msg': 'No active account matching given email.',
                    'account_is_locked': False,
                    'error': True
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        """
        Check if the requested user has been locked. Include a link for password 
        reset in the response.
        """

        if requested_user.is_locked:
            return Response(
                {
                    'msg': 'Too many failed login attempts within a short period of time.',
                    'account_is_locked': True,
                    'error': True
                },
                status=status.HTTP_404_NOT_FOUND
            )

        
        """
        Check if the credentials given match those on file. If so, reset the failed attempts
        and return Access and Refresh tokens.
        """

        password_is_correct = requested_user.check_password(given_pswd)

        if password_is_correct:
            refresh = RefreshToken.for_user(requested_user)

            # Delete failed attempts to reset counter
            FailedLoginAttempt.objects.filter(attempted_owner=requested_user).delete()

            return Response(
                {
                    'msg': 'Successful login attempt',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'account_is_locked': False,
                    'expires_in': refresh.lifetime,
                    'error': False
                },
                status=status.HTTP_200_OK
            )
        else:

            """
            If the login attempt has failed, check how many failed attempts have occured
            in the last five minutes and lock the account if neccesary. Include a link for password 
            reset in the response.
            """

            five_minutes_ago = timezone.now() + timezone.timedelta(minutes=-5)
            failed_attempt = FailedLoginAttempt(attempted_owner=requested_user)
            failed_attempt.save()

            attempts_last_five_minutes = len(FailedLoginAttempt.objects.filter(attempted_at__gte=five_minutes_ago))
            attempts_exceed_limit = True if (attempts_last_five_minutes >= 5) else False

            if attempts_exceed_limit:
                requested_user.is_locked = True
                requested_user.save()

            return Response(
                {
                    'msg': f'Failed login attempt',
                    'failed attempts': f'{attempts_last_five_minutes}',
                    'account_is_locked': attempts_exceed_limit,
                    'error': True
                },
                status=status.HTTP_403_FORBIDDEN
            )

class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]


    def get(self, request, format=None):
        data = request.data

        given_refresh_token = data["refresh"]
        try:
            refresh_token = RefreshToken(given_refresh_token)
            res = {
                "access": str(refresh_token.access_token),
                "expires_in": refresh_token.lifetime,
                "error": False,
            }

            return Response(data=res, status=status.HTTP_200_OK)
        except:
            res = {
                "msg": "The given refresh token was invalid.",
                "error": True
            }
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    """
    Setup password reset.
    """
    pass



# class 

# ## TODO
# # 1. Activate User Account via Email
# # 2. Add login view to issue token and handle incorrect password limit
# # 3. Create a link for password reset and include that in the response. 
# # This will prevent another unneccesary http request.