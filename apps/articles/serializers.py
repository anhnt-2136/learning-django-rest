from rest_framework import serializers

from apps.articles.models import Article
from apps.tags.models import Tag


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    tag_list = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "slug",
            "title",
            "description",
            "tags",
            "tag_list",
            "created_at",
            "updated_at",
            "author",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "slug": {"required": False},
        }

    def get_tag_list(self, obj):
        return [{"name": tag.name} for tag in obj.tags.all()]

    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "bio": obj.author.bio,
            "image": obj.author.image,
        }

    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        article = Article.objects.create(**validated_data)
        tag_objs = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        article.tags.set(tag_objs)
        return article
