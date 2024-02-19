from typing import Any, Union, Dict

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema

from .models import Blog, Post, Subscription
from .serializers import PostSerializer


@swagger_auto_schema(
    method='post',
    responses={200: 'Подписка оформлена', 404: 'Блог не найден', 400: 'Нельзя подписаться на свой блог'},
    operation_summary='Подписаться на блог пользователя',
)
@api_view(['POST'])
def subscribe_to_blog(request: Any, blog_id: int) -> Response:
    """
    Подписаться на блог пользователя.

    :param request: Запрос пользователя.
    :param blog_id: Идентификатор блога, на который пользователь хочет подписаться.
    :return: Сообщение об успешной подписке или ошибке.
    """
    try:
        blog = get_object_or_404(Blog, id=blog_id)
    except Http404:
        return Response({'error': 'Блог не найден'}, status=404)

    if request.user.blog != blog:
        subscription, created = Subscription.objects.get_or_create(user=request.user, blog=blog)
        if created:
            return Response({'message': f'Вы подписались на {blog}'}, status=200)
        else:
            return Response({'message': f'Вы уже подписаны на {blog}'}, status=200)
    else:
        return Response({'error': 'Нельзя подписываться на свой собственный блог'}, status=400)


@swagger_auto_schema(
    method='post',
    responses={200: 'Подписка отменена', 404: 'Подписка не была найдена', 400: 'Блог не найден'},
    operation_summary='Отписаться от блога пользователя',
)
@api_view(['POST'])
def unsubscribe_from_blog(request: Any, blog_id: int) -> Response:
    """
    Отписаться от блога пользователя.

    :param request: Запрос пользователя.
    :param blog_id: Идентификатор блога, от которого пользователь хочет отписаться.
    :return: Сообщение об успешной отписке или ошибке.
    """
    try:
        blog = get_object_or_404(Blog, id=blog_id)
    except Http404:
        return Response({'error': 'Блог не найден'}, status=404)

    subscriptions = Subscription.objects.filter(user=request.user, blog_id=blog_id)
    if subscriptions.exists():
        subscriptions.delete()
        return Response({'message': f'Подписка отменена для {blog}'}, status=200)
    else:
        return Response({'error': 'Подписка не была найдена'}, status=404)


@swagger_auto_schema(
    method='get',
    responses={200: 'OK'},
    pagination_class=PageNumberPagination,
    operation_summary='Новостная лента',
)
@api_view(['GET'])
def news_feed(request: Any) -> Union[Response, Dict[str, Any]]:
    """
    Персональная лента новостей пользователя.

    :param request: Запрос пользователя.
    :return: Персональная лента новостей пользователя.
    """
    subscriptions = Subscription.objects.filter(user=request.user)
    subscribed_blogs = [subscription.blog for subscription in subscriptions]
    posts = Post.objects.filter(blog__in=subscribed_blogs).order_by('-created_at')[:500]
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(page_posts, many=True)

    return paginator.get_paginated_response(serializer.data)

