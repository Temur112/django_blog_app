
from django.contrib import admin
from django.urls import path, include
from post import urls as post_urls
from django.contrib.sitemaps.views import sitemap
from post.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(post_urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
