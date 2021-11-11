from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
]
