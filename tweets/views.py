from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Tweet

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"
