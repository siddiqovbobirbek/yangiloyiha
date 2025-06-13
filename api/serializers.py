from rest_framework.serializers import ModelSerializer
from articles.models import Article
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model  = User
        fields = ['username', 'email']
        


class ArticleSerializer(ModelSerializer):
    # author = UserSerializer()
    class Meta: 
        model  = Article
        fields = ['id', 'author', 'title', 'body', 'date', 'photo']
        