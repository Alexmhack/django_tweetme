from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Tweet

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"

def tweet_list_view(request):
	objects = Tweet.objects.all()
	context = {
		'objects': objects
	}

	return render(request, 'tweets/list_view.html', context)
