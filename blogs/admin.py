from django.contrib import admin

from .models import Blog, Post


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
    search_fields = ['user', 'id']

