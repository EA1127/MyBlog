from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрированы на сайте'
