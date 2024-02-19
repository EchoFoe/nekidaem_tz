from rest_framework import serializers

from .models import Subscription, Post


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'blog', 'title', 'content', 'created_at']
