from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'links/$', LinkListView.as_view(), name='links'),
]
