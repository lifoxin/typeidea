from django.conf.urls import url
from .views import *
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'rss|feed/', LatestPostFeed(), name='rss'),
	url(r'sitemap\.xml$', sitemap_views.sitemap, {'sitemaps':{'posts':PostSitemap}}),
	url(r'search/$', SearchView.as_view(), name='search'),
	url(r'author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
	url(r'category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
	url(r'tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
	url(r'post/(?P<post_id>\d+).html', PostDetailView.as_view(), name='post-detail'),
	url(r'link/$', links, name='links'),
]
