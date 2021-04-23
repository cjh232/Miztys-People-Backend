from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **other_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, phone, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
            
        return self.create_user(email, first_name, last_name, phone, password, **other_fields)




class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    is_locked = models.BooleanField(default=False)

    # Required by Django for superuser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    objects = CustomUserManager() # Define that we're using a custom account manager
    
    USERNAME_FIELD = 'email'  # Set the unique identifying field
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

  
class Profile(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_on_email_list = models.BooleanField(default=False)
    experience = models.TextField(max_length=300, default="")

    def __str__(self):
        return f"{self.owner.get_full_name()}'s Profile"


class FailedLoginAttempt(models.Model):
    attempted_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

