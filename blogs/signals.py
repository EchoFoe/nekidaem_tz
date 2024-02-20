from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post
from .tasks import update_news_feed


@receiver(post_save, sender=Post)
def post_saved(sender, instance, created, **kwargs):
    if created:
        update_news_feed.delay(instance.id)


@receiver(post_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    update_news_feed.delay(instance.id)

