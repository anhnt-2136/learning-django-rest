from django.db import models
from slugify import slugify

from apps.tags.models import Tag
from apps.users.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.author = User.objects.first()  # TODO: Implement logic to set the author based on the request context

        print("Model.save()", self.author)
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
