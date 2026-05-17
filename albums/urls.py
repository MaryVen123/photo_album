from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('photos/add/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
]
