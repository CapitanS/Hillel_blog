from django.contrib import admin

from .models import Comment, Post, RSSPost


def make_moderated(modeladmin, request, queryset):
    queryset.update(moderated=True)
make_moderated.short_description = "Mark selected comments as moderated"  # noqa:E305


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['username', 'text', 'post', 'moderated']
    list_display = ('username', 'text', 'moderated')
    list_filter = ('moderated', 'username')
    actions = [make_moderated]


class CommentInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'short_description', 'image', 'full_description', 'user', 'posted']
    inlines = [CommentInlineModelAdmin]
    list_filter = ('posted', 'user')
    list_display = ('title', 'short_description', 'user', 'posted')


@admin.register(RSSPost)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'link']
    list_display = ('title', 'link')

