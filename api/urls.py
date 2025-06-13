from django.urls import path
from .views import ArticleListAPIView, ArticleDetailAPIView

app_name = 'api'
urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='list'),
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='detail'),
    # path('create/', ArticleCreateAPIView.as_view(), name='create'),
]
