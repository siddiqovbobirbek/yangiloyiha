from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255, blank=True)
    body = RichTextField()
    photo = models.ImageField(upload_to='images/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.id)])

    @property
    def like_count(self):
        return self.likes.count()


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ('article', 'user', 'session_key')

    def __str__(self):
        return f"{self.user or self.session_key} -> {self.article}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    izoh = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} - {self.izoh[:20]}"

    def __str__(self):
        return self.izoh

    def get_absolute_url(self):
        return reverse('article_list')

    @property
    def like_count(self):
        return self.likes.count()


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    # class Meta:
    #     unique_together = ('article', 'user', 'session_key')
