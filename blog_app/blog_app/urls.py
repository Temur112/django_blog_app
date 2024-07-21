
from django.contrib import admin
from django.urls import path, include
from post import urls as post_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(post_urls)),
]
