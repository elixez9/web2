from django import forms
from .models import Post


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
