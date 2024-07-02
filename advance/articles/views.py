from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, RedirectView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, DetailView
from .forms import RegisterForm, ArticleForm, UserFavouriteArticleForm
from .models import Article, UserFavouriteArticle
from django.http import HttpResponse


class Articles(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.all().order_by('-created')


class Home(RedirectView):
    url = '/article/'


class Login(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')


class Publications(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class Detail(LoginRequiredMixin, DetailView):
        model = Article
        template_name = 'ArticleDetailView.html'

        def post(self, request, *args, **kwargs):
            user = request.user
            article = get_object_or_404(Article, id=request.POST.get('article_id'))
            if not UserFavouriteArticle.objects.filter(user=user, article=article).exists():
                UserFavouriteArticle.objects.create(user=user, article=article)
            return redirect('favorites')


class Logout(LogoutView):
    next_page = 'home'


class Favorites(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'FavoriteArticlesView.html'
    context_object_name = 'favorite_articles'

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user)


class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_login = timezone.now()
        self.object.save()
        return super().form_valid(form)


class Publish(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'publish.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article-list')


class add_to_favorites(CreateView):
    model = UserFavouriteArticle
    form_class = UserFavouriteArticleForm
    template_name = 'add_to_favorites.html'
    def form_valid(self, form):
        print("Form lol")
        form.instance.user = self.request.user
        form.instance.article = get_object_or_404(Article, id=self.request.POST.get('article_id'))
        if UserFavouriteArticle.objects.filter(user=self.request.user, article=form.instance.article).exists():
            self.template_name = 'already_in_favorites.html'
        else:
            print("Form is valid")  # Debug print statement
            response = super().form_valid(form)
            if self.object.pk:
                print("Data saved successfully")  # Debug print statement
            else:
                print("Data not saved")  # Debug print statement
            return response
    def form_invalid(self, form):
        print("Form is not valid")  # Debug print statement
        print(form.errors)  # Print form errors
        return super().form_invalid(form)