from django.shortcuts import render

from .models import Tweet

def tweet_detail_view(request, id=None):
	object = Tweet.objects.get(id=id)
	context = {
		'object': object
	}

	return render(request, 'detail.html', context)
