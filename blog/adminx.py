from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin

import xadmin
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
	form = PostAdminForm
	list_display = ['title', 'category', 'status', 'created_time', 'owner','operator']
	list_display_links = []
	exclude = ('html','owner','pv','uv')

	list_filter = ['category','title','owner'] #注意这里不是定义的filter类，而是字段名
	search_fields = ['title', 'category__name']

	actions_on_top = True
	actions_on_bottom = True
	#编辑页面
	save_on_top = True

	form_layout = (
		Fieldset('基础信息',Row("title","category"),'status','tag',),
		Fieldset('内容信息','desc', 'is_md', 'content_md','content_ck','content')
	)

	filter_vertical = ('tag',)	
	def operator(self, obj):
		return format_html('<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,)))
	operator.short_description = '操作'

@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
	list_display = ('name', 'status', 'is_nav', 'created_time')
	fields = ('name', 'status', 'is_nav')

@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name', 'status', 'created_time')
	fields = ('name', 'status')

class PostInline:
	form_layout = (Container(Row("title", "desc"),))
	extra = 1 #控制额外多几个
	model = Post
