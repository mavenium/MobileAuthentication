from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import transaction

from . import models


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            widget=forms.TextInput(attrs={'autofocus': True}),
            label=self.fields['username'].label,
            help_text='شماره موبایل کاربر',
            required=True,
            max_length=11,
            validators=[RegexValidator(
                regex=r'09(\d{9})$',
                message="مثال : 09000000000",
            )],
            error_messages=({
                'required': 'لطفاً مقدار نام کاربری را وارد نمایید.',
            }),
        )

        self.fields['password1'].required = False
        self.fields['password2'].required = False

        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(SignUpForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("مقدار گذرواژه و تأیید گذرواژه را وارد نمایید.")
        return password2

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_active = False
        user.save()
        self.request.session['username'] = user.username
        return user


class VerifyForm(forms.Form):
    verification_code = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        label="کد تأیید",
        help_text='کد تأیید ارسالی به شماره موبایل',
        validators=[RegexValidator(
            regex=r'^[0-9]+$',
            message="مثال : 00000",
        )],
        error_messages=({
            'required': 'لطفاً کد تأیید را وارد نمایید.',
            'invalid': 'فقط عدد قابل قبول است!',
        }),
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        label="نام کاربری",
        help_text='شماره موبایل کاربر',
        validators=[RegexValidator(
            regex=r'09(\d{9})$',
            message="مثال : 09000000000",
        )],
        error_messages=({
            'required': 'لطفاً نام کاربری را وارد نمایید.',
        }),
    )


class ProfileForm(forms.Form):
    GENDER_CHOICES = [
        (0, 'آقا'),
        (1, 'خانم'),
    ]
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام'}),
        label='نام',
        max_length=64,
        required=False,
        error_messages=({
            'required': 'لطفاً نام خود را وارد نمایید!',
            'invalid': 'مقدار وارد شده صحیح نمی باشد!',
        }),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
        label='نام خانوادگی',
        max_length=128,
        required=False,
        error_messages=({
            'required': 'لطفاً نام خانوادگی خود را وارد نمایید!',
            'invalid': 'مقدار وارد شده صحیح نمی باشد!',
        }),
    )
    date_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'تاریخ تولد'}),
        label='تاریخ تولد',
        help_text='تاریخ تولد کاربر',
        required=False,
        error_messages=({
            'required': 'لطفاً مقدار تاریخ تولد را وارد نمایید.',
            'invalid': 'مقدار وارد شده صحیح نمی باشد!',
        }),
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='جنسیت',
        required=False,
        error_messages=({
            'invalid': 'مقدار وارد شده صحیح نمی باشد!',
        }),
    )
