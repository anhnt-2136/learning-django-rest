from rest_framework import serializers

from apps.tags.models import Tag

from .models import Article


class TagsField(serializers.Field):
    """
    Custom field to handle tags for both input and output
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)

    def to_representation(self, value):
        """Convert tags to output format"""
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        """Convert input data to internal format"""
        if not isinstance(data, list):
            raise serializers.ValidationError("Tags must be a list")

        for item in data:
            if not isinstance(item, str):
                raise serializers.ValidationError("Each tag must be a string")

        return data


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "body",
            "tags",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "slug", "author"]

    def get_author(self, obj):
        print(obj.author)
        return {
            "username": obj.author.username,
            "bio": obj.author.bio,
            "image": obj.author.image,
        }

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        tag_names = validated_data.pop("tags", [])
        article = Article.objects.create(**validated_data)

        if tag_names:
            tag_objs = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            article.tags.set(tag_objs)

        return article

    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tags", [])

        # Update article fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update tags
        if tag_names:
            tag_objs = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            instance.tags.set(tag_objs)

        return instance
