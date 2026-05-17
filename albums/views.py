from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Album, Photo
from .forms import PhotoForm, AlbumForm


class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(Q(is_public=True) | Q(owner=user))


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'

    def get_object(self, queryset=None):
        album = super().get_object(queryset)
        if not album.is_public and album.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You do not have permission to view this album')
        return album


class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = getattr(self, 'object', None)
        if obj is None:
            # for CreateView
            return True
        user = self.request.user
        return user.is_staff or obj.owner == user


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'


class AlbumDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('albums:album-list')


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_initial(self):
        initial = super().get_initial()
        album_pk = self.request.GET.get('album')
        if album_pk:
            initial['album'] = get_object_or_404(Album, pk=album_pk)
        return initial

    def get_success_url(self):
        return self.object.album.get_absolute_url()


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def test_func(self):
        photo = self.get_object()
        return self.request.user.is_staff or photo.album.owner == self.request.user

    def get_success_url(self):
        return self.object.album.get_absolute_url()
