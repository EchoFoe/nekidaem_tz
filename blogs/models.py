from django.db import models
from django.conf import settings

from .bases import DateTimeBaseModel


class Blog(models.Model):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='blog', db_index=True,
                                verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'Блог пользователя: {self.user.username}'


class Post(DateTimeBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', db_index=True, verbose_name='Блог')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=140, blank=True, verbose_name='Текст', help_text='Не более 140 символов')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'Пост {self.title} пользователя: {self.blog.user.username}'


class Subscription(DateTimeBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions',
                             db_index=True, verbose_name='Пользователь')
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE, related_name='subscribers', db_index=True,
                             verbose_name='Блог')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'blog')

    def __str__(self):
        return f'{self.user} подписан на блог {self.blog}'


class ReadPost(DateTimeBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_posts_by_user',
                             db_index=True, verbose_name='Пользователь')
    post = models.ForeignKey('blogs.Post', on_delete=models.CASCADE, related_name='read_by_user', db_index=True,
                             verbose_name='Пост')
    is_read = models.BooleanField(default=False, verbose_name='Прочитан?')

    class Meta:
        verbose_name = 'Прочтенный пост'
        verbose_name_plural = 'Прочтенные посты'
        unique_together = ('user', 'post')
