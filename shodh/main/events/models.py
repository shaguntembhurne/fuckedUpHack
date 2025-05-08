from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('announcement', 'Announcement'),
        ('urgent', 'Urgent'),
        ('research', 'Research'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")

    # 🔥 New fields
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🎯 Targeting feature
    target_branches = models.JSONField(blank=True, null=True)
    target_years = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title
