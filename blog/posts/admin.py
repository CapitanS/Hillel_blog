from django.contrib import admin
from .models import Post, Comment


class CommentInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'short_description', 'image', 'full_description', 'borrower', 'posted']
    inlines = [CommentInlineModelAdmin]


admin.site.register(Post, PostAdmin)
