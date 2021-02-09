from django.contrib import admin

from .models import Comment, Post


def make_moderated(modeladmin, request, queryset):
    queryset.update(moderated=True)
make_moderated.short_description = "Mark selected comments as moderated"  # noqa:E305


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['username', 'text', 'moderated']
    list_display = ('username', 'text', 'moderated')
    list_filter = ('moderated',)
    actions = [make_moderated]


class CommentInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'short_description', 'image', 'full_description', 'user', 'posted']
    inlines = [CommentInlineModelAdmin]
