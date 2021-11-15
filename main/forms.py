from datetime import datetime

from django import forms

from .models import News, Image, Comment


class NewsForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = News
        fields = ('title', 'content', 'category', 'user', 'created',)
        # exclude = ('user', )


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        # fields = '__all__'
        fields = ('image', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
