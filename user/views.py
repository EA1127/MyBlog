from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import RegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрированы на сайте!'


class SignInView(LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('home')


def profile(request):
    return render(request, 'user/profile.html')
