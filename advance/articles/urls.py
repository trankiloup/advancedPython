from django.urls import path
from .views import ArticleListView, HomeView, UserLoginView, CustomLogoutView, FavoriteArticlesView, \
    RegisterView, PublishView, WhatIPublishView, ArticleDetailView, add_to_favorites

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', WhatIPublishView.as_view(), name='WhatIPublishView'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('favorites/', FavoriteArticlesView.as_view(), name='favorites'),
    path('register/', RegisterView.as_view(), name='register'),
    path('publish/', PublishView.as_view(), name='publish'),
    path('detail/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),
]