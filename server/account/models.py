# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import *

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.validators import MinValueValidator, validate_comma_separated_integer_list
from django.db import models
from django.dispatch import receiver

from multiselectfield import MultiSelectField
from rest_framework.authtoken.models import Token


SUPPORTED_COINS = (
    ('bitcoin', 'Bitcoin'),
    ('bitcoin_cash', 'Bitcoin Cash'),
    ('dash', 'Dash'),
    ('ethereum', 'Ethereum'),
    ('ethereum_classic', 'Ethereum Classic'),
    ('litecoin', 'Litecoin'),
    ('monero', 'Monero'),
    ('neo', 'NEO'),
    ('ripple', 'Ripple'),
    ('zcash', 'Zcash')
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first name, last name,
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name, last
        name, and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        # __unicode__ on Python 2
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_score = models.IntegerField(default=0)
    coins = MultiSelectField(choices=SUPPORTED_COINS, null=True, blank=True)

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(models.signals.post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create an authentication token for new users
    """
    if created:
        Token.objects.create(user=instance)

class Coin(models.Model):
    """
    All coins supported on Polyledger.
    """
    symbol = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True)
    image = models.FilePathField(path='account/static/account/img/coins/', null=True)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    """
    A user's portfolio containing coins.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd = models.FloatField(default=0)
    coins = models.ManyToManyField(Coin)

    def __str__(self):
        return '{0}\'s portfolio'.format(self.user)

    def coin_list(self):
        return ', '.join([coin.name for coin in self.coins.all()])

class Holding(models.Model):
    """
    A holding of a coin in a portfolio.
    """
    coin = models.OneToOneField(Coin)
    amount = models.FloatField(default=0.0)
    portfolio = models.ForeignKey(Portfolio)
