from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Account


class AccountCreateAPIViewTest(APITestCase):
    """
    Тесты для представления AccountCreateAPIView.

    Проверяют создание нового пользователя и попытку создания уже существующего пользователя.
    """

    def test_create_account(self) -> None:
        """
        Проверка создания нового пользователя.
        """
        url: str = reverse('account-create')
        data: dict = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_account(self) -> None:
        """
        Проверка попытки создания существующего пользователя.
        """
        url: str = reverse('account-create')
        data: dict = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailAPIViewTest(APITestCase):
    """
    Тесты для представления UserDetailAPIView.

    Проверяют получение информации о пользователе по его имени и ID,
    а также попытку получения информации о несуществующем пользователе.
    """

    def setUp(self) -> None:
        """
        Подготовка данных для тестирования.
        """
        self.user: Account = Account.objects.create(username='test_user', password='test_password')

    def test_get_user_by_username(self) -> None:
        """
        Проверка получения информации о пользователе по его имени.
        """
        url: str = reverse('user-detail-by-username', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self) -> None:
        """
        Проверка получения информации о пользователе по его ID.
        """
        url: str = reverse('user-detail-by-id', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_user_by_username(self) -> None:
        """
        Проверка попытки получения информации о несуществующем пользователе по его имени.
        """
        url: str = reverse('user-detail-by-username', kwargs={'username': 'nonexistent_username'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_user_by_id(self) -> None:
        """
        Проверка попытки получения информации о несуществующем пользователе по его ID.
        """
        url: str = reverse('user-detail-by-id', kwargs={'user_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
