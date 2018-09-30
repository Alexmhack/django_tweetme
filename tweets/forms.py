from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	# content = forms.CharField(
	# 	label='',
	# 	widget=forms.Textarea(
	# 		attrs={
	# 			"rows": 5,
	# 			"placeholder": "Tweet here",
	# 			"class": "form-control form-control-lg"
	# 		}
	# 	)
	# )

	class Meta:
		model = Tweet
		fields = ("content",)
		exclude = ("user",)

	# def clean_content(self):
	# 	data = self.cleaned_data["content"]
	# 	if "fuck" in data:
	# 		raise forms.ValidationError("Cannot have offensive content")

	# 	return data
