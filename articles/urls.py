from django.urls import path
from . import views

from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleCreateView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    toggle_like,
    
)

urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment_new'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('<int:pk>/toggle_like/', toggle_like, name='toggle_like'),
    path('articles/article/<int:article_id>/rate/', views.rate_article, name='rate_article'),


  
]
