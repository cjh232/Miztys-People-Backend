from django.core.mail import EmailMessage, send_mail
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import jwt

class VerificationTokenGenerator(PasswordResetTokenGenerator):
    pass

class EmailUtil:

    @staticmethod
    def send_mail(data, to):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=to)
        email.send()


class AccountVerificationUtil:
    
    @staticmethod
    def send_activation_email(user, request):
        generate_token = VerificationTokenGenerator()
        token = generate_token.make_token(user)
        current_site = get_current_site(request).domain

        relative_link=reverse('verify_email')
        absolute_url=f'http://{current_site+relative_link}?user_id={user.id}&token={token}'

        url = f'http://localhost:3000/verify?token={token}&user_id={user.id}'

        email_body = f'Hi {user.first_name} {user.last_name}!\nUse link below to verfiy your email\n{url}'

        data={
            'body': email_body,
            'subject': 'Verfiy your email'
        }

        EmailUtil.send_mail(data, [user.email])


    @staticmethod
    def validate_activation_token(user, token):
        token_generator = VerificationTokenGenerator()
        return token_generator.check_token(user, token)



def blacklist_token(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist() 
        return True
    except:
        return False




