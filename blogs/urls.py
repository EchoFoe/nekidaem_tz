from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/<int:blog_id>/', views.subscribe_to_blog, name='subscribe_to_blog'),
    path('unsubscribe/<int:blog_id>/', views.unsubscribe_from_blog, name='unsubscribe_from_blog'),
    path('news-feed/', views.news_feed, name='news_feed'),
]