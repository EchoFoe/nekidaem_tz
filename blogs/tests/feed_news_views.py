from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Post, ReadPost
from accounts.models import Account


class NewsFeedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create(username='test_user')

    def test_news_feed(self):
        """
        Тестирование получения новостной ленты пользователя.
        """
        url = reverse('news_feed')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MarkAsReadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create(username='test_user')
        self.post = Post.objects.create(title='Test Post', content='Test Content')

    def test_mark_posts_as_read(self):
        """
        Тестирование прочитанного поста пользователем.
        """
        url = reverse('mark-posts-as-read')
        self.client.force_authenticate(user=self.user)
        data = {'post_ids': [self.post.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
