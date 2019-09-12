from django.shortcuts import render,redirect,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from .forms import CommentForm

class CommentView(TemplateView):
	http_method_names = ['post',]
	template_name = 'comment/result.html'
	
	def post(self, request, *args, **kwargs):
		comment_form = CommentForm(request.POST)
		target = request.POST.get('target')

		if comment_form.is_valid():
			instance = comment_form.save(commit=False)
			instance.target = target
			instance.save()
			succeed = True
			print("target is:",target)
		#	return redirect(target) 评论在当前页
		
		else:
			succeed = False

		context = {'succeed':succeed, 'form':comment_form, 'target':target,}
		print(context)
		# 评论在其他页，再跳转
		return self.render_to_response(context)
