from django import forms
from .models import Article, Comment


class ArticleCreationForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'score', 'movie', ]
        # exclude = ['user',]


class ArticleMovieCreationForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'score', ]
        # exclude = ['user',]


class ArticleUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'score']
        # exclude = ['user',]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['article', 'user', ]