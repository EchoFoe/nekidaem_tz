import random
import string

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from random import choice
from tqdm import tqdm  # Импорт библиотеки для прогресс-бара

from blogs.models import Blog, Post, ReadPost
from accounts.models import Account

fake = Faker()


def generate_username():
    # Генерация случайного имени пользователя из случайных букв и цифр
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Началась загрузка данных в БД...'))

        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Загрузка аккаунтов и блогов'))
            self.create_accounts(10)
            self.stdout.write(self.style.SUCCESS('Загрузка постов'))
            self.create_posts(50)

        self.stdout.write(self.style.SUCCESS('Загрузка данных прошла успешно!'))

    def create_accounts(self, num_accounts):
        # Используем tqdm для отображения прогресса
        for _ in tqdm(range(num_accounts), desc='Создание аккаунтов с блогами', unit=' accounts'):
            username = generate_username()
            email = fake.email()
            password = fake.password()
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone = fake.phone_number()[:15]
            date_of_birth = fake.date_of_birth()

            account = Account.objects.create_user(username=username, email=email, password=password,
                                                  first_name=first_name, last_name=last_name, phone=phone,
                                                  date_of_birth=date_of_birth)

            blog = Blog.objects.create(user=account)

    def create_blogs(self):
        pass

    def create_posts(self, num_posts):
        blogs = Blog.objects.all()
        for _ in tqdm(range(num_posts), desc='Создание постов', unit=' posts'):
            blog = choice(blogs)
            title = fake.sentence()
            content = fake.paragraph()
            post = Post.objects.create(blog=blog, title=title, content=content)
