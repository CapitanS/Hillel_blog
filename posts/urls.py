from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/update/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.post_comments, name='post_comments'),
    path('my-posts/', views.users_posts, name='users_posts'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('user/', views.UserList.as_view(), name='user_list'),
]
