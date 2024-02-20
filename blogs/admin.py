from django.contrib import admin

from .models import Blog, Post, Subscription, ReadPost


class PostInline(admin.StackedInline):
    """ Класс-хелпер для отображения объектов Post, связанных с Blog """

    model = Post
    extra = 1
    verbose_name_plural = 'Посты к блогу'
    verbose_name = 'Пост к блогу'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Заголовок', {'fields': ('title',)}),
        ('Контент поста', {'fields': ('content',)}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """ Админ-панель для Blog """

    save_as = True
    inlines = [PostInline]
    list_display = ['id', 'user']
    list_display_links = ['id']
    list_per_page = 30
    search_fields = ['user', 'id']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """ Админ-панель для Subscription """

    save_as = True
    list_display = ['id', 'user', 'blog']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30
    list_display_links = ['id']


@admin.register(ReadPost)
class ReadPostAdmin(admin.ModelAdmin):
    """ Админ-панель для ReadPost """

    save_as = True
    list_display = ['id', 'post', 'user', 'is_read']
    list_per_page = 30
    readonly_fields = ['created_at', 'updated_at']
    list_display_links = ['post']
