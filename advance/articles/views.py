from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, RedirectView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, DetailView
from .forms import RegisterForm, ArticleForm
from .models import Article, UserFavouriteArticle
from django.http import HttpResponse

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'


class HomeView(RedirectView):
    url = '/articles/'


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')


class WhatIPublishView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'ArticleDetailView.html'
    context_object_name = 'article'


class CustomLogoutView(LogoutView):
    next_page = 'home'


class FavoriteArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'FavoriteArticlesView.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(userfavouritearticle__user=self.request.user)


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save(commit=False)
        self.object.last_login = timezone.now()
        self.object.save()
        return super().form_valid(form)


class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'publish.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article-list')


@require_POST
def add_to_favorites(request):
    article_id = request.POST.get('article_id')
    article = Article.objects.get(id=article_id)
    # Check if the user has already added this article to their favorites
    if UserFavouriteArticle.objects.filter(user=request.user, article=article).exists():
        # If the article is already in the user's favorites, return a message
        return HttpResponse('This article is already in your favorites.')
    else:
        # If the article is not in the user's favorites, add it
        UserFavouriteArticle.objects.create(user=request.user, article=article)
        return redirect('favorites')
