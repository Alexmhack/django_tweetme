from django.db import models

class Tweet(models.Model):
	content = models.TextField()
