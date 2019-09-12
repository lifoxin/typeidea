from datetime import date
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView,ListView
from django.db.models import Q,F 
from django.core.cache import cache

from .models import Post, Tag, Category
from django.contrib.auth.models import User
from config.models import SideBar
from comment.forms import CommentForm
from comment.models import Comment

class CommonViewMixin:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'sidebars':SideBar.get_all(),})
		context.update(Category.get_navs())
		return context

class PostDetailView(CommonViewMixin, DetailView):
	queryset = Post.latest_posts()
	template_name = 'blog/detail.html'	
	context_object_name = 'post'
	pk_url_kwarg = 'post_id'

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		self.handle_visited()
		return response

	def handle_visited(self):
		increase_pv = False
		increase_ur = False
		uid = self.request.uid
		pv_key = 'pv:%s:%s' % (uid, self.request.path)
		uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
		if not cache.get(pv_key):
			increase_pv = True
			cache.set(pv_key, 1, 1*60)  #1 分钟有效

		if not cache.get(uv_key):
			increase_uv = True
			cache.set(pv_key, 1, 24*60*60) # 24小时有效

		if increase_pv and increase_uv:
			Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
		elif increase_pv:
			Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
		elif increase_uv:
			Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)


class IndexView(CommonViewMixin, ListView):
	"""
	queryset属性：设定基础的数据集,可以通过以下方法过滤
	template_name 指定模块路径
	"""
	queryset = Post.latest_posts()
	"""一页显示多少栏"""
	paginate_by = 4  
	context_object_name = 'post_list'
	template_name = 'blog/list.html'


class SearchView(IndexView):
	def get_context_data(self):
		context = super().get_context_data()
		context.update({'keyword':self.request.GET.get('keyword','')})
		return context

	def get_queryset(self):
		queryset = super().get_queryset()
		keyword = self.request.GET.get('keyword')
		if not keyword:
			return queryset
		return queryset.filter(Q(title__icontains=keyword)|Q(desc__icontains=keyword)| Q(content__icontains=keyword))

class AuthorView(IndexView):
	def get_context_data(self):
		context = super().get_context_data()
		owner_id = self.kwargs.get('owner_id')
		owner = get_object_or_404(User, pk=owner_id)
		context.update({'owner':owner,})
		return context
	
	def get_queryset(self):
		queryset = super().get_queryset()
		author_id = self.kwargs.get('owner_id')
		return queryset.filter(owner_id=author_id)

class CategoryView(IndexView):
	def get_context_data(self, **kwargs):
		"""
		get_context_data 获取渲染到模板中的所有上下文，
		有新增数据需要传递到模板中，可以重写改方法完成。
		self.kwargs中的数据其实是从url定义的参数取得的
		"""
		context= super().get_context_data(**kwargs)
		category_id = self.kwargs.get('category_id')
		category = get_object_or_404(Category, pk=category_id)
		context.update({'category':category,})
		return context
	
	def get_queryset(self):
		"""
		get_queryset 用来获取数据,如果设定了queryset,
		则会直接返回queryset
		"""
		queryset = super().get_queryset()
		category_id = self.kwargs.get('category_id')
		return queryset.filter(category_id=category_id)	

class TagView(IndexView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tag_id = self.kwargs.get('tag_id')
		tag = get_object_or_404(Tag, pk=tag_id)
		context.update({'tag':tag,})
		return context

	def get_queryset(self):
		"""重写 queryset， 根据标签过滤"""
		queryset = super().get_queryset()
		tag_id = self.kwargs.get('tag_id')
		return queryset.filter(tag__id=tag_id)

def links(request):
	return HttpResponse('links')
