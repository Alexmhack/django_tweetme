from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Tweet
from .forms import TweetModelForm

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"


class TweetCreateView(CreateView):
	form = TweetModelForm

