import logging
from celery import shared_task

from accounts.models import Account
from .models import Post

logger = logging.getLogger('django')


@shared_task
def update_news_feed(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        logger.warning(f'Пост с id={post_id} не существует.')
        return

    subscribed_users = Account.objects.filter(subscriptions__blog=post.blog)

    for user in subscribed_users:
        subscribed_posts = Post.objects.filter(blog__in=user.subscriptions.values_list('blog', flat=True))
        user.read_posts.add(*subscribed_posts)

    logger.info(f'Лента новостей успешно обновлена для {subscribed_users.count()} пользователей.')


@shared_task
def send_daily_newsletter():
    subscribers = Account.objects.all()
    for subscriber in subscribers:
        latest_posts = Post.objects.filter(blog__in=subscriber.subscriptions.values_list('blog', flat=True)) \
                                    .order_by('-created_at')[:5]
        if latest_posts:
            logger.info(f'Ежедневная отправка для {subscriber.username}:')
            logger.info('Последние посты:')
            for post in latest_posts:
                logger.info(f'Пост {post.title} пользователя: {post.blog.user.username}')
