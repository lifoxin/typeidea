"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from blog.apis import PostViewSet,CategoryViewSet

from .autocomplete import CategoryAutocomplete, TagAutocomplete

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
	url(r'^',include('blog.urls',namespace='main')),
	url(r'^',include('config.urls',namespace='config')),
	url(r'^',include('comment.urls',namespace='comment')),
	url(r'^',include('user.urls',namespace='user')),
	url(r'^admin/', admin.site.urls),
	url(r'^login/', xadmin.site.urls,name='xadmin'),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^api/', include(router.urls)),
	url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
	url(r'^ckeditor/',include('ckeditor_uploader.urls')),
	url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(),name='category-autocomplete'),
	url(r'^tag-autocomplete/$', TagAutocomplete.as_view(),name='tag-autocomplete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns = [
		url(r'^debug/', include(debug_toolbar.urls)),
		url(r'^silk/',include('silk.urls',namespace='silk')),
	] + urlpatterns
