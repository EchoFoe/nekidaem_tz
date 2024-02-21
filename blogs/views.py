from typing import Any, Union, Dict, List

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Blog, Post, Subscription, ReadPost
from .serializers import PostSerializer

BLOGS = 'Блоги'
NEWS_FEED = 'Новостная лента'


@swagger_auto_schema(
    tags=[BLOGS],
    method='post',
    responses={200: 'Подписка оформлена', 404: 'Блог не найден', 400: 'Нельзя подписаться на свой блог'},
    operation_summary='Подписаться на блог пользователя',
)
@api_view(['POST'])
def subscribe_to_blog(request: Any, blog_id: int) -> Response:
    """
    Подписка на блог пользователя.

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
    tags=[BLOGS],
    method='post',
    responses={200: 'Подписка отменена', 404: 'Подписка не была найдена', 400: 'Блог не найден'},
    operation_summary='Отписаться от блога пользователя',
)
@api_view(['POST'])
def unsubscribe_from_blog(request: Any, blog_id: int) -> Response:
    """
    Отписка от блога пользователя.

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
    methods=['get'],
    tags=[NEWS_FEED],
    responses={200: 'OK', 404: 'Нет подписок'},
    pagination_class=PageNumberPagination,
    operation_summary='Новостная лента',
)
@api_view(['GET'])
def news_feed(request: Any) -> Union[Response, Dict[str, Any]]:
    """
    Вывод ленты последних 500 постов, с пагинацией 10 объектов на представлении.

    :param request: Запрос пользователя.
    :return: Ответ сервера.
    """
    if request.method == 'GET':
        subscriptions = Subscription.objects.filter(user=request.user)
        if not subscriptions:
            return Response({'message': 'Пользователь не подписан ни на один блог'}, status=status.HTTP_404_NOT_FOUND)

        subscribed_blogs = [subscription.blog for subscription in subscriptions]
        posts = Post.objects.filter(blog__in=subscribed_blogs).order_by('-created_at')[:500]
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page_posts, many=True)
        return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='post',
    tags=[NEWS_FEED],
    responses={
        200: 'OK',
        404: 'Пост с указанным ID не найден',
        400: 'Пост уже помечен как прочитанный/не переданы в теле запроса IDs'
    },
    operation_summary='Пометить посты как прочитанные',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'post_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER)
            ),
        },
        required=['post_ids'],
    ),
)
@api_view(['POST'])
def mark_posts_as_read(request: Dict[str, Union[Any, List[int]]]) -> Response:
    """
    Помечает выбранные посты как прочитанные.

    :param request: Запрос пользователя.
    :return: Ответ сервера.
    """
    post_ids = request.data.get('post_ids', [])

    if not post_ids:
        return Response({'error': 'Не переданы идентификаторы постов'}, status=status.HTTP_400_BAD_REQUEST)

    posts_not_found = []
    posts_already_read = []

    for post_id in post_ids:
        try:
            post = Post.objects.get(id=post_id)
            if ReadPost.objects.filter(user=request.user, post=post, is_read=True).exists():
                posts_already_read.append(post_id)
            else:
                ReadPost.objects.create(user=request.user, post=post, is_read=True)
        except Post.DoesNotExist:
            posts_not_found.append(post_id)

    if posts_not_found:
        return Response({'error': f'Посты с IDs: {posts_not_found} не найдены'}, status=status.HTTP_404_NOT_FOUND)

    if posts_already_read:
        return Response({'error': f'Посты с IDs: {posts_already_read} уже помечены как прочитанные'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'Посты c IDs: {post_ids} успешно помечены как прочитанные'},
                    status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=[BLOGS],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'content'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'content': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: 'Пост добавлен', 404: 'Блог не найден или пользователь не имеет прав на добавление поста'},
    operation_summary='Добавить пост в блог',
)
@api_view(['POST'])
def add_post_to_blog(request: Any, blog_id: int) -> Response:
    """
    Добавление поста в блог пользователя.

    :param request: Запрос пользователя.
    :param blog_id: Идентификатор блога, в который пользователь хочет добавить пост.
    :return: Сообщение о добавлении поста или ошибке.
    """
    try:
        blog = get_object_or_404(Blog, id=blog_id)
    except Http404:
        return Response({'error': 'Блог не найден'}, status=404)

    if blog.user != request.user:
        return Response({'error': 'Вы можете добавлять посты только в свой собственный блог'}, status=400)

    request.data['blog'] = blog_id
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': f'Пост успешно добавлен в {blog}'}, status=200)
    else:
        return Response(serializer.errors, status=400)


@swagger_auto_schema(
    tags=[BLOGS],
    method='post',
    responses={200: 'Пост удален', 404: 'Пост не найден или пользователь не имеет прав на удаление'},
    operation_summary='Удалить пост из блога',
)
@api_view(['POST'])
def delete_post_from_blog(request: Any, post_id: int) -> Response:
    """
    Удаление поста из блога пользователя.

    :param request: Запрос пользователя.
    :param post_id: Идентификатор поста, который пользователь хочет удалить.
    :return: Сообщение об удалении поста или ошибке.
    """
    try:
        post = Post.objects.filter(id=post_id, blog__user=request.user).first()
    except Post.DoesNotExist:
        return Response({'error': 'Посты не найдены'}, status=404)

    if post is None:
        return Response({'error': 'Вы не можете удалять этот пост, так как он не принадлежит вашему блогу'}, status=404)

    post.delete()
    return Response({'message': 'Пост успешно удален'}, status=200)
