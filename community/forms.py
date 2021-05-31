from django import forms
from .models import Article, Comment


class ArticleMovieCreationForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'score', 'image']
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