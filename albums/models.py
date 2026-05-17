from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary.models import CloudinaryField

User = get_user_model()


class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('albums:album-detail', args=[str(self.pk)])


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('image')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Photo {self.pk} in {self.album.title}'

    def get_absolute_url(self):
        return self.album.get_absolute_url()
