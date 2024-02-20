from django.test import TestCase
from django.core.management import call_command

from accounts.models import Account
from blogs.models import Blog, Post


class PopulateDatabaseTestCase(TestCase):
    def test_populate_database(self):
        call_command('prepopulate_data')

        self.assertEqual(Account.objects.count(), 1000)
        self.assertEqual(Blog.objects.count(), 1000)
        self.assertEqual(Post.objects.count(), 5000)
