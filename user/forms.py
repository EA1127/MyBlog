from django import forms
from django.conf import settings
from django.core.mail import send_mail

from user.models import User


def send_welcome_email(email):
    message = f'You were successfully registered at MyBlog! Thanks for the interest in our site!'
    send_mail(
        'Registration at MyBlog',
        message,
        'myblogadmin@gmail.com',
        [email],
        fail_silently=False
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name', 'image')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данной почтой уже существует')
        return email

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.pop('password_confirmation')
        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        send_welcome_email(user.email)
        return user
