from rest_framework import permissions


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsMatchArticleSlug(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow non-detail routes without checking object
        return True

    def has_object_permission(self, request, view, obj):
        url_slug = view.kwargs.get("article_slug")
        return obj.article.slug == url_slug
