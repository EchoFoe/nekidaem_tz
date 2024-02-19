from django.db import models
from .bases import DateTimeBaseModel


class Blog(models.Model):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='blog')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'Блог пользователя: {self.user.username}'


class Post(DateTimeBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', verbose_name='Блог')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=140, blank=True, verbose_name='Текст', help_text='Не более 140 символов')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'Пост {self.title} пользователя: {self.blog.user.username}'
