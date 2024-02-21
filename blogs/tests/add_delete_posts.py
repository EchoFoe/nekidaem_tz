from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Blog, Post
from accounts.models import Account


class BlogAPITestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='test_user', password='test_password')
        self.blog = Blog.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.test_data = {'title': 'Тестовый пост', 'content': 'Тестовый контент.'}

    def test_add_post_to_blog(self):
        url = reverse('add-post-to-blog', args=[self.blog.id])
        data = self.test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, self.test_data['title'])
        self.assertEqual(Post.objects.first().content, self.test_data['content'])

    def test_delete_post_from_blog(self):
        post = Post.objects.create(blog=self.blog, title=self.test_data['title'], content=self.test_data['content'])
        url = reverse('delete-post-from-blog', args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)
