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
from rest_framework import routers

from apps.articles.views import ArticleViewSet
from apps.tags.views import TagViewSet
from apps.users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="users")
router.register("tags", TagViewSet, basename="tags")
router.register("articles", ArticleViewSet, basename="articles")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]
