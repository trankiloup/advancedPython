from django.urls import path
from .views import add_to_favorites, Home, Login, Articles, Logout, \
    Publish, Detail, Register, Favorites, Publications

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('article/', Articles.as_view(), name='article-list'),
    path('article/<int:pk>/', Publications.as_view(), name='Publications'),
    path('logout/', Logout.as_view(), name='logout'),
    path('favorites/', Favorites.as_view(), name='favorites'),
    path('register/', Register.as_view(), name='register'),
    path('publish/', Publish.as_view(), name='publish'),
    path('detail/<int:pk>/', Detail.as_view(), name='article-detail'),
    path('add_to_favorites/', add_to_favorites.as_view(), name='add_to_favorites'),
]