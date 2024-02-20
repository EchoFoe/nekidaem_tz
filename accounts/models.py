from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Account(AbstractUser):
    groups = models.ManyToManyField(Group, verbose_name='Группы', blank=True, related_name='user_accounts')
    user_permissions = models.ManyToManyField(Permission, verbose_name='Разрешения пользователя', blank=True,
                                              related_name='user_accounts')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    surname = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    read_posts = models.ManyToManyField('blogs.Post', blank=True, related_name='read_by')

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'Пользователь: {self.username}'

    def get_full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    def get_fio(self):
        name_components = [self.first_name, self.last_name, self.surname]
        formatted_components = [component.capitalize() for component in name_components if component]
        return ' '.join(formatted_components)
