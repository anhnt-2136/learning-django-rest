from rest_framework import serializers

from apps.articles_favorites.models import ArticleFavorite


class ArticleFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = ArticleFavorite
        fields = ["article", "user"]

    def validate(self, attrs):
        """
        Check if user has already favorited this article.
        """
        # Get article and user from context (passed from view)
        article = self.context.get("article")
        request = self.context.get("request")
        user = request.user if request else None

        if not article or not user:
            raise serializers.ValidationError("Article and user are required.")

        # Check for existing favorite
        if ArticleFavorite.objects.filter(article=article, user=user).exists():
            raise serializers.ValidationError(
                "You have already favorited this article."
            )

        return attrs

    def get_user(self, obj):
        """
        Return the username of the user who favorited the article.
        """
        return obj.user.username if obj.user else None

    def get_article(self, obj):
        """
        Return the title of the favorited article.
        """
        return obj.article.title if obj.article else None
