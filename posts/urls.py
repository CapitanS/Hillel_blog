from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


app_name = 'posts'
urlpatterns = [
    path('', cache_page(1000)(views.index), name='index'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/update/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),
    path('posts/', cache_page(5)(views.PostList.as_view()), name='post_list'),
    path('posts/<int:pk>/', cache_page(10)(views.post_detail), name='post_detail'),
    path('my-posts/', views.users_posts, name='users_posts'),
    path('user/<int:pk>', cache_page(15)(views.user_detail), name='user_detail'),
    path('user/', cache_page(5)(views.UserList.as_view()), name='user_list'),
    path('feedback', views.feedback_form, name="feedback"),
]
