from django import forms
from django.forms import inlineformset_factory

from .models import Post, PostPhoto


class SignInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input100', 'name': 'username', 'placeholder': 'Enter username'}),
        max_length=100, required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'name': 'pass', 'placeholder': 'Enter password'}),
        required=False)


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = []
        # localized_fields = '__all__'
        fields = ['title', 'slug', 'author', 'content', 'status', ]
        # widgets = {
        #     'photo': forms.ClearableFileInput(attrs={'multiple': True})
        # }

    # def __init__(self, author, *args, **kwargs):
    #     super(PostAddForm, self).__init__(*args, **kwargs)
    #     self.author = author


class PhotoForm(forms.ModelForm):
    class Meta:
        model = PostPhoto
        exclude = ('post',)
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'multiple': False})
        }


PostPhotoFormSet = inlineformset_factory(
    Post, PostPhoto, form=PhotoForm, fields=['photo'], extra=1, can_delete=False)
