from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from apps.users.validators import domen_name, email_name

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=256,
        required=True,
        validators=[domen_name, email_name]
    )

    class Meta:
        model = User
        fields = (
            'username', 'password'
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'phone', 'name', 'password1', 'password2'
        )


class ConfForm(forms.ModelForm):
    secret_key = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('secret_key',)
