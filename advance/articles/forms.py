# advance/articles/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author']