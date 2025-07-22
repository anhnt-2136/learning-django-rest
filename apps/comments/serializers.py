from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "created_at",
            "updated_at",
            "article",
            "owner",
            "author",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
