from django import forms
from .models import Post


class CreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
