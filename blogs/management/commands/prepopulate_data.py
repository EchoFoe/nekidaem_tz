import random
import string

from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from random import choice
from tqdm import tqdm

from blogs.models import Blog, Post
from accounts.models import Account

fake = Faker()


def generate_username() -> str:
    """ Генерация случайного имени пользователя. """
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        """ Хелпер по хендлеру """
        self.stdout.write(self.style.SUCCESS('Началась загрузка данных в БД...'))

        with transaction.atomic():
            self.create_accounts(200)
            self.create_posts(1000)

        self.stdout.write(self.style.SUCCESS('Загрузка данных прошла успешно!'))

    def create_accounts(self, num_accounts: int) -> None:
        """ Создание аккаунтов с их блогами. """
        self.stdout.write(self.style.SUCCESS('Загрузка аккаунтов и блогов'))
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

    def create_posts(self, num_posts: int) -> None:
        """ Создание постов. """
        self.stdout.write(self.style.SUCCESS('Загрузка постов'))
        blogs: List[Blog] = Blog.objects.all()
        for _ in tqdm(range(num_posts), desc='Создание постов', unit=' posts'):
            blog = choice(blogs)
            title = fake.sentence()
            content = fake.paragraph()
            post = Post.objects.create(blog=blog, title=title, content=content)
