from django import forms

from captcha.fields import CaptchaField
import mistune
from .models import Comment

class CommentForm(forms.ModelForm):
	nickname = forms.CharField(
		label='昵称',
		max_length=50,
		widget=forms.widgets.Input(attrs={'class':'form-control','style':"width:60%;"})
		)
	email = forms.CharField(
		label='Email',
		max_length=50,
		widget=forms.widgets.EmailInput(attrs={'class':'form-control','style':"width:60%;"})
		)
	website = forms.CharField(
		label='网站',
		max_length=100,
		widget=forms.widgets.URLInput(attrs={'class':'form-control','style':"width:60%;"})
	)
	content = forms.CharField(
		label='内容',
		max_length=500,
		widget=forms.widgets.Textarea(attrs={'rows':6,'cols':6,'class':'form-control'})
	)
	captcha = CaptchaField()	

	def clean_content(self):
		content = self.cleaned_data.get('content')
		content = mistune.markdown(content)
		if len(content) < 1:
			raise forms.ValidationError('内容字数少于10')
		return content

	class Meta:
		model = Comment
		fields = ['nickname','email','website','content',]
