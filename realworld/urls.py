"""
URL configuration for realworld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.articles.views import ArticleViewSet
from apps.articles_favorites.views import ArticleFavoritesViewSet
from apps.comments.views import CommentViewSet
from apps.registration.views import UserRegistrationViewSet
from apps.tags.views import TagViewSet
from apps.users.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("tags", TagViewSet)
router.register("articles", ArticleViewSet)

comments_router = NestedDefaultRouter(router, "articles", lookup="article")
comments_router.register(
    "comments",
    CommentViewSet,
    basename="article-comments",
)

articles_favorites_router = NestedDefaultRouter(
    router,
    "articles",
    lookup="article",
)
articles_favorites_router.register(
    "favorites",
    ArticleFavoritesViewSet,
    basename="article-favorites",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(comments_router.urls)),
    path("api/", include(articles_favorites_router.urls)),
    path("api/user", UserViewSet.as_view(), name="current-user"),
    path(
        "api/login",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/register",
        UserRegistrationViewSet.as_view(),
        name="user-register",
    ),
]
