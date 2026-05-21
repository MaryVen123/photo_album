from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .models import Photo, Album


class PhotoForm(forms.ModelForm):
    image = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff'])
        ]
    )

    class Meta:
        model = Photo
        fields = ['album', 'image', 'caption']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            valid_mime_types = [
                'image/jpeg',
                'image/png',
                'image/gif',
                'image/webp',
                'image/bmp',
                'image/tiff',
            ]
            content_type = getattr(image, 'content_type', None)
            if content_type and content_type not in valid_mime_types:
                raise forms.ValidationError('Only image files are allowed.')
        return image


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
