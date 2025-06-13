from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article, Comment, ArticleLike
from django.urls import reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = context['articles']
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key or self.request.session.create()

        # Har bir maqolaga `has_liked` atributini qo‘shamiz
        for article in articles:
            article.has_liked = article.likes.filter(
                user=user if user else None,
                session_key=None if user else session_key
            ).exists()
        
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['parent_comments'] = article.comments.filter(parent__isnull=True)
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        # Faqat parent izohlar
        context['parent_comments'] = article.comments.filter(parent__isnull=True).order_by('id')

        user = self.request.user
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        context['has_liked'] = ArticleLike.objects.filter(
            article=article,
            user=user if user.is_authenticated else None,
            session_key=None if user.is_authenticated else session_key
        ).exists()

        return context
    
        

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'article_edit.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    
    
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comment, Article
from django.urls import reverse_lazy

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['izoh']
    template_name = 'comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['izoh']
    template_name = 'comment_edit.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user



from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Comment
from .forms import CommentForm

def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    article = parent_comment.article

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.article = article
            reply.parent = parent_comment
            reply.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    return render(request, 'reply_form.html', {'form': form, 'parent': parent_comment})


from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Article, ArticleLike

@require_POST
def toggle_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    user = request.user if request.user.is_authenticated else None

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # 👇 Faqat user yoki session_keydan biri ishlatiladi
    like_qs = ArticleLike.objects.filter(
        article=article,
        user=user if user else None,
        session_key=None if user else session_key
    )

    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        ArticleLike.objects.create(
            article=article,
            user=user if user else None,
            session_key=None if user else session_key
        )
        liked = True

    like_count = ArticleLike.objects.filter(article=article).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})
