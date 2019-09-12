from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .form import LoginForm
from .models import User

def register(request):
	return render(request,'user/register.html')

def register_hander(request):
	user = User.objects.all()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			username = cleaned_data['username']
			email = cleaned_data['email']
			mobile = cleaned_data['mobile']
			password = cleaned_data['password']
			user = User.objects.create_superuser(
					username=username, email=email, 
					mobile=mobile, password=password
					)
			user.is_staff = True # 可选，有权限登录admin
			user.save()
			print("注册成功")
			return render(request,'user/tips.html')
		else:
			errors = form.errors
			print(errors)
			return render(request,'user/register.html',{'errors':errors})
	return redirect('/')
