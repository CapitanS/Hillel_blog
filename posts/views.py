from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    template_name = 'posts/post_create_page.html'
    success_url = reverse_lazy('posts:post_list')

    def get_form_kwargs(self):
        kwargs = super(PostCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Post()
        kwargs['instance'].user = self.request.user
        return kwargs


class PostList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/post_list_page.html'


def post_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.all().filter(post=post)
    paginator = Paginator(comments, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():
            comm = Comment()
            comm.username = form.cleaned_data['username']
            comm.text = form.cleaned_data['text']
            comm.post = post
            comm.save()
            return HttpResponseRedirect(reverse('posts:post_comments', args=(post.id,)))

    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post,
        'page_obj': page_obj,
    }

    return render(request, 'posts/post_detail_page.html', context)
