from rest_framework import viewsets

from .models import Post,Category
from .serializers import (
	PostSerializer,PostDetailSerializer,
	CategorySerializer,CategoryDetailSerializer
)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
	"""提供文章接口"""
	serializer_class = PostSerializer
	queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

	def retrieve(self, request, *args, **kwargs):
		self.serializer_class = PostDetailSerializer
		return super().retrieve(request, *args, **kwargs)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
	"""提供分类接口"""
	serializer_class = CategorySerializer
	queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

	def retrieve(self, request, *args, **kwargs):
		self.serializer_class = CategoryDetailSerializer
		return super().retrieve(request, *args, **kwargs)
