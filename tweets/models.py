from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Tweet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

	def clean(self, *args, **kwargs):
		content = self.content
		if "fuck" in content:
			raise ValidationError("Cannot have offensive content")

		return super().clean()
