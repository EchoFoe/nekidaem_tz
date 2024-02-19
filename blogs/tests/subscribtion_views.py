from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Blog, Post, Subscription
from accounts.models import Account


class BlogSubscriptionTestCase(TestCase):
    """
    Тесты для подписки на блоги и новостной ленты пользователей.
    """

    def setUp(self):
        """
        Устанавливаем начальные данные для тестов.
        """
        self.client = APIClient()
        self.user = Account.objects.create(username='test_user')
        self.blog = Blog.objects.create(user=self.user)
        self.test_user2 = Account.objects.create(username='test_user2')
        self.blog2 = Blog.objects.create(user=self.test_user2)

    def test_subscribe_to_blog(self):
        """
        Тестирование подписки на блог пользователя.
        """
        url = reverse('subscribe_to_blog', kwargs={'blog_id': self.blog2.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe_to_own_blog(self):
        """
        Тестирование попытки подписки на собственный блог.
        """
        url = reverse('subscribe_to_blog', kwargs={'blog_id': self.blog.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscribe_from_blog(self):
        """
        Тестирование отписки от блога пользователя.
        """
        subscription = Subscription.objects.create(user=self.user, blog=self.blog2)
        url = reverse('unsubscribe_from_blog', kwargs={'blog_id': self.blog2.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsubscribe_from_non_existing_subscription(self):
        """
        Тестирование отписки от несуществующей подписки.
        """
        url = reverse('unsubscribe_from_blog', kwargs={'blog_id': self.blog2.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_feed(self):
        """
        Тестирование получения новостной ленты пользователя.
        """
        post = Post.objects.create(blog=self.blog2, title='Test Post', content='Test Content')
        Subscription.objects.create(user=self.user, blog=self.blog2)
        url = reverse('news_feed')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
