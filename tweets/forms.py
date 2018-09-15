from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = "__all__"
		# exclude = ("user",)

	# def clean_content(self):
	# 	data = self.cleaned_data["content"]
	# 	if "fuck" in data:
	# 		raise forms.ValidationError("Cannot have offensive content")

	# 	return data
