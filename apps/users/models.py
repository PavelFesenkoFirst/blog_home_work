from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from random import randint

# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, phone, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(
            email=email, phone=phone, is_staff=is_staff,
            is_superuser=is_superuser, date_joined=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, phone, password, **extra_fields):
        return self._create_user(
            email, phone, password, False, False, **extra_fields
        )


    def create_superuser(self, email, phone, password, **extra_fields):
        return self._create_user(
            email, phone, password, True, True, **extra_fields
        )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    secret_key = models.CharField(max_length=5, verbose_name='ключ активации')
    confirm = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'custom user'
        verbose_name_plural = 'custom users'

    def email_user(self, subject, message, **kwargs):
        send_mail(
            subject, message, settings.EMAIL_HOST_USER, [self.email], **kwargs
        )

    def s_key(self):
        self.secret_key = randint(10000, 99999)

    def get_absolute_url(self):
        return reverse('blog_home_work:author-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

