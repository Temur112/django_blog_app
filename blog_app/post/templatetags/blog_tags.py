from django import template
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


@register.simple_tag(name='post_count')
def total_posts():
    return Post.published_.count()


@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published_.order_by('-published')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag(name='most_commented')
def most_commented(count=5):
    return Post.published_.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_text(text):
    return mark_safe(markdown.markdown(text))
