from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from .forms import CommentForm, FeedbackFrom, RegisterForm
from .models import Comment, Post

User = get_user_model()


def index(request):
    """View function for home page of site."""

    return render(request, 'posts/index.html')


class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('posts:index')
    success_message = 'Profile created'

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('posts:index')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


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

    def get_queryset(self):
        return Post.objects.all().filter(posted=True)


# paginator!
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, posted=True)
    comments = Comment.objects.all().filter(post=post).filter(moderated=True)
    paginator = Paginator(comments, 2)

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
            return HttpResponseRedirect(reverse('posts:post_detail', args=(post.id,)))

    else:
        initial = {'username': request.user.username}
        form = CommentForm(initial=initial)

    context = {
        'form': form,
        'post': post,
        'page_obj': page_obj,
    }

    return render(request, 'posts/post_detail_page.html', context)


def users_posts(request):
    current_user = request.user

    posted_posts = Post.objects.filter(user=current_user).filter(posted=True)
    paginator = Paginator(posted_posts, 2)
    page_number = request.GET.get('page')
    page_obj_posted = paginator.get_page(page_number)

    unposted_posts = Post.objects.filter(user=current_user).filter(posted=False)
    paginator = Paginator(unposted_posts, 2)
    page_number = request.GET.get('page')
    page_obj_unposted = paginator.get_page(page_number)

    context = {
        'page_obj_posted': page_obj_posted,
        'page_obj_unposted': page_obj_unposted,
    }
    return render(request, 'posts/users_posts_page.html', context)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update_page.html'
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    success_url = reverse_lazy('posts:post_list')

    def get_object(self, queryset=None):
        obj = super(PostUpdate, self).get_object()
        if not obj.user == self.request.user:
            return redirect(obj)
        return obj


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:post_list')
    template_name = 'posts/post_delete_page.html'

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if not obj.user == self.request.user:
            return redirect(obj)
        return obj


# paginator!
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk, is_staff=False)
    posts = Post.objects.filter(user=user).filter(posted=True)
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'obj': user,
    }
    return render(request, 'posts/user_detail_page.html', context)


class UserList(ListView):
    model = User
    template_name = 'posts/user_list_page.html'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


def feedback_form(request):
    if request.method == "GET":
        form = FeedbackFrom()
    else:
        form = FeedbackFrom(request.POST)
        if form.is_valid():
            subject = 'New feedback!'
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(subject, message, from_email, ['admin@example.com'])

            return redirect('posts:feedback')
    return render(
        request,
        "posts/feedback_page.html",
        context={
            "form": form,
        }
    )
