from django import forms
from .models import Photo, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'image', 'caption']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']
