from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ("content",)
		excluce = ("user",)
