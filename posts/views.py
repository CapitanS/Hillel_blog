from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Post, Comment


# Create your views here.
def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    template_name = 'posts/post_create_page.html'
    #success_url = reverse_lazy('posts:post_list')


class PostList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/post_list_page.html'
