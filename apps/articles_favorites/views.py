from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.articles.models import Article
from apps.articles_favorites.models import ArticleFavorite
from apps.articles_favorites.permissions import IsOwner
from apps.articles_favorites.serializers import ArticleFavoriteSerializer
from apps.core.mixins import (
    CustomCreateMixin,
    CustomGenericViewSet,
)


class ArticleFavoritesViewSet(
    CustomCreateMixin,
    CustomGenericViewSet,
):
    """
    A simple ViewSet for managing article favorites.
    """

    serializer_class = ArticleFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        return ArticleFavorite.objects.filter(
            article__slug=self.kwargs["article_slug"]
        ).select_related("article")

    def get_serializer_context(self):
        """Override to pass additional context to serializer"""
        context = super().get_serializer_context()

        # Get the article from URL parameter
        article_slug = self.kwargs.get("article_slug")
        if article_slug:
            self.article = get_object_or_404(Article, slug=article_slug)
            context["article"] = self.article

        return context

    def get_permissions(self):
        """
        Instantiate and return the list of permissions required for this view.
        """
        if self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article=self.article)

    def delete(self, request, *args, **kwargs):
        """
        Custom DELETE method to handle DELETE /favorites (without pk)
        """
        article_slug = self.kwargs.get("article_slug")
        article = get_object_or_404(Article, slug=article_slug)

        # Find and delete the user's favorite for this article
        try:
            favorite = ArticleFavorite.objects.get(
                article=article, user=request.user
            )
            favorite.delete()
            return self.response(status=status.HTTP_204_NO_CONTENT)
        except ArticleFavorite.DoesNotExist:
            return self.response(
                {"detail": "You haven't favorited this article"},
                status=status.HTTP_404_NOT_FOUND,
            )
