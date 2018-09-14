from django.shortcuts import render

from .models import Tweet

def tweet_detail_view(request, id=None):
	object = Tweet.objects.get(id=id)
	context = {
		'object': object
	}

	return render(request, 'tweets/detail_view.html', context)


def tweet_list_view(request):
	objects = Tweet.objects.all()
	context = {
		'objects': objects
	}

	return render(request, 'tweets/list_view.html', context)
