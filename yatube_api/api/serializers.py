from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts import models


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = models.Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = models.Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = models.Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all(),
    )

    class Meta:
        fields = ('user', 'following')
        model = models.Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=('user', 'following',)
            )
        ]

    def validate(self, data):
        following = data.get('following')
        user = self.context['request'].user
        if user == following:
            raise serializers.ValidationError(
                'You can\'t subscribe to yourself'
            )
        return data
