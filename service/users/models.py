from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomUserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('пожалуйста введите правильный адрес почты')
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if email:

            email = self.normalize_email(email)
            self.email_validator(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name





