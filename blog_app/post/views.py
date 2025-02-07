from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from post.models import Post
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    model = Post
    queryset = Post.published_.all().prefetch_related('author')
    context_object_name = 'posts'
    template_name = 'post/list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        tag_slug = self.kwargs.get('tag_slug')
        print(tag_slug)
        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = Post.published_.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        # tag = None
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('tag_slug') is not None:
            tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
            context['tag'] = tag
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/detail.html'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')

        obj = get_object_or_404(queryset, published__year=year, published__month=month, published__day=day, slug=slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_ids_list = self.object.tags.values_list('id', flat=True)
        similar_posts = Post.published_.all().filter(tags__in=tag_ids_list).exclude(id=self.object.pk)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:4]
        context['comment_form'] = CommentForm()
        context['comment_list'] = self.object.comments.filter(active=True)
        context['similar_posts'] = similar_posts
        return context


def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status='PB')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f'{cd["name"]}: {cd["email"]} '
                       f'recommends you read {post.title}')
            message = (
                f'Read {post.title} at {post_url} \n\n'
                f'{cd["name"]}\'s comments {cd["comments"]}'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status='PB')
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'post/comment.html', {'post': post, 'form': form, 'comment': comment})
