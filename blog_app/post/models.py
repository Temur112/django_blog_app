from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    tags = TaggableManager()
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, unique_for_date='published')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')

    objects = models.Manager()
    published_ = PublishedManager()

    class Meta:
        ordering = ['-published']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [models.Index(fields=['-published']),]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog_app:post_detail',
            args=[
                self.published.year,
                self.published.month,
                self.published.day,
                self.slug
            ]
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Commented by {self.name} on {self.post}"