from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'register_hander/$', register_hander, name='register_hander'),
	url(r'register/$', register, name='register'),
]
