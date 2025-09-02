from django.urls import path
from .views import (BlogListView, BlogDetailView,
 BlogCreateView, BlogUpdateView, delete_post)




urlpatterns = [
	path('', BlogListView.as_view(), name='posts_list'),
	path('create_post/', BlogCreateView.as_view(), name='create_post'),
	path('posts/<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
	path('posts/<slug:slug>/update', BlogUpdateView.as_view(), name='update_post'),
	path('posts/<slug:slug>/delete', delete_post, name='delete_post'),
]


