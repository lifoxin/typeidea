from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'comment/$', CommentView.as_view(), name='comment-list'),
]
