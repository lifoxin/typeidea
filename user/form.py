from django import forms
from captcha.fields import CaptchaField
from .models import User

class LoginForm(forms.ModelForm):
	username = forms.CharField(
					required=True,min_length=2,
					error_messages={
						'required':'必填用户名',
						'min_length':'至少2字符'
					}
				)
	password = forms.CharField(
					required=True,min_length=8,
					error_messages={
						'required':'必填密码',
						'min_length':'至少8字符'
					}
				)
#	captcha = CaptchaField()	

	def clean_data(self):
		mobile = self.cleaned_data['mobile']
		user = User.objects.filter(username=self.cleaned_data.get('username')).first()
		if not mobile.isdigit():
			raise forms.ValidationError('必须是数字')
		if	user:
			raise forms.ValidationError('该账户已注册')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ('username', 'mobile', 'email', 'password')
