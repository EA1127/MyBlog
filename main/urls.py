from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:slug>/', blog_category_detail, name='category'),
    path('news-detail/<int:pk>/', news_detail, name='detail'),
    path('add-news/', add_news, name='add-news'),
    path('update-news/<int:pk>/', update_news, name='update-news'),
    path('delete-news/<int:pk>/', delete_news, name='delete-news'),
]

