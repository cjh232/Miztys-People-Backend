from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.token_blacklist.management import flushexpiredtokens

def my_cron_job():
    