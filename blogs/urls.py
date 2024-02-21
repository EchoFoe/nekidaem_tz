from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/<int:blog_id>/', views.subscribe_to_blog, name='subscribe-to-blog'),
    path('unsubscribe/<int:blog_id>/', views.unsubscribe_from_blog, name='unsubscribe-from-blog'),
    path('news-feed/', views.news_feed, name='news_feed'),
    path('mark-post-as-read/', views.mark_posts_as_read, name='mark-posts-as-read'),
    path('delete-post-from-blog/<int:post_id>/', views.delete_post_from_blog, name='delete-post-from-blog'),
    path('add-post-to-blog/<int:blog_id>', views.add_post_to_blog, name='add-post-to-blog'),
]
