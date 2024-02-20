from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Blog, Subscription

from accounts.models import Account


class NewsFeedTestCase(APITestCase):
    """
    Тесты для новостной ленты.

    Проверяют наличие новостной ленты с подпиской и отсутствия подписок.
    """
    def setUp(self):

        self.user = Account.objects.create_user(username='test_user', password='test_password')
        self.user2 = Account.objects.create_user(username='test_user2', password='test_password2')
        self.blog1 = Blog.objects.create(user=self.user)
        self.blog2 = Blog.objects.create(user=self.user2)

    def test_news_feed_with_subscriptions(self):
        """
        Проверка подписки.
        """
        Subscription.objects.create(user=self.user, blog=self.blog1)
        Subscription.objects.create(user=self.user, blog=self.blog2)

        self.client.force_authenticate(user=self.user)

        url = reverse('news_feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)

    def test_news_feed_without_subscriptions(self):
        """
        Проверка отсутствия подписки.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('news_feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('message' in response.data)
