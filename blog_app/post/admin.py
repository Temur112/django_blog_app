from django.contrib import admin

from .models import Post, Comment


class CommentAdminTabular(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdminManager(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'title', 'slug', 'author', 'status', 'published')
    list_display_links = ('id', 'title',)
    readonly_fields = ('id', 'published')
    search_fields = ('published', 'slug', 'title')
    list_filter = ('published', 'status')
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['status', 'published']
    raw_id_fields = ('author',)
    show_facets = admin.ShowFacets.ALWAYS
    inlines = [CommentAdminTabular]


@admin.register(Comment)
class CommentAdminManager(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'post', 'name', 'email', 'created')
    list_display_links = ('id', 'name',)
    list_filter = ('active', 'name')
    search_fields = ('name', 'email', 'body')
    raw_id_fields = ('post',)
    show_facets = admin.ShowFacets.ALWAYS



