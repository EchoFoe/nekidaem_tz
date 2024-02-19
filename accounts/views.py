from typing import Any, Dict, Union, Optional

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import get_object_or_404

from .models import Account
from .serializers import AccountCreateSerializer, AccountSerializer


class AccountCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Request'},
    )
    def post(self, request, *args, **kwargs) -> Union[Response, Dict[str, Any]]:
        """
        Создание нового пользователя.

        :param request: Запрос, содержащий данные пользователя.
        :type request: rest_framework.request.Request
        :return: Ответ с данными созданного пользователя или ошибку, если данные невалидны.
        :rtype: Union[Response, Dict[str, Any]]
        """
        data: Dict[str, Any] = request.data
        serializer = AccountCreateSerializer(data=data)
        if serializer.is_valid():
            username: str = data.get('username')
            if Account.objects.filter(username=username).exists():
                return Response({'error': 'Пользователь с таким именем уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            response_data = {'username': user.username}
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        responses={200: 'OK', 400: 'Invalid Request', 404: 'Not Found'},
        operation_summary='Получение информации о пользователе',
    )
    def get(self, request, username: Optional[str] = None, user_id: Optional[int] = None) -> Response:
        """
        Получение информации о пользователе.

        :param request: Запрос.
        :type request: rest_framework.request.Request
        :param username: Имя пользователя.
        :type username: str or None
        :param user_id: Идентификатор пользователя.
        :type user_id: int or None
        :return: Информация о пользователе или сообщение об ошибке, если пользователь не найден.
        :rtype: Response
        """
        if username:
            return self.get_by_username(request, username)
        elif user_id:
            return self.get_by_id(request, user_id)
        else:
            return Response(
                {'error': 'Имя пользователя или ID должны быть указаны'}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_by_username(self, request, username: str) -> Response:
        """
        Получение информации о пользователе по его имени.

        :param request: Запрос.
        :type request: rest_framework.request.Request
        :param username: Имя пользователя.
        :type username: str
        :return: Информация о пользователе или сообщение об ошибке, если пользователь не найден.
        :rtype: Response
        """
        user = get_object_or_404(Account, username=username)
        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_by_id(self, request, user_id: int) -> Response:
        """
        Получение информации о пользователе по его ID.

        :param request: Запрос.
        :type request: rest_framework.request.Request
        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Информация о пользователе или сообщение об ошибке, если пользователь не найден.
        :rtype: Response
        """
        user = get_object_or_404(Account, id=user_id)
        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
