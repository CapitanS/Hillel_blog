from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.post_comments, name='post_comments'),
    path('my-posts/', views.users_posts, name='users_posts'),
]
