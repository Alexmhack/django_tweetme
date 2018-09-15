from django.contrib import admin

from .models import Tweet
from .forms import TweetModelForm

# admin.site.register(Tweet)

class TweetModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Tweet
		form = TweetModelForm


admin.site.register(Tweet, TweetModelForm)
