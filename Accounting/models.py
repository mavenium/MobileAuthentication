from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        (0, 'آقا'),
        (1, 'خانم'),
    ]
    username = models.CharField(
        verbose_name='نام کاربری',
        help_text='شماره موبایل کاربر',
        max_length=11,
        unique=True,
        null=False,
        blank=False,
        validators=[RegexValidator(
            regex=r'09(\d{9})$',
            message="مثال : 09000000000",
        )]
    )
    date_of_join = models.DateField(
        verbose_name='تاریخ عضویت',
        help_text='تاریخ عضویت در سامانه',
        auto_now_add=True,
        null=False,
        blank=False
    )
    date_of_birth = models.DateField(
        verbose_name='تاریخ تولد',
        help_text='تاریخ تولد کاربر',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name='فعال',
        help_text='فعال بودن حساب کاربری در سامانه',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='دستری به بخش مدیریت',
        help_text='کاربر بتواند به بخش مدیریت سیستم دسترسی داشته باشد',
        default=False
    )
    first_name = models.CharField(
        verbose_name='نام',
        help_text='نام کاربر',
        max_length=64,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='نام خانوادگی',
        help_text='نام خانوادگی کاربر',
        max_length=128,
        null=True,
        blank=True
    )
    gender = models.PositiveSmallIntegerField(
        verbose_name='جنسیت',
        help_text='جنسیت کاربر',
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    verification_code = models.CharField(
        verbose_name='کد فعال سازی',
        help_text='کد فعال سازی ارسال شده شماره موبایل',
        max_length=5,
        editable=False,
        null=True,
        blank=True
    )

    object = managers.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_gender(self):
        return self.GENDER_CHOICES[self.gender][1]
