from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"
	login_url = "/admin"


class TweetUpdateView(UpdateView):
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	success_url = "/tweet/tweets"
