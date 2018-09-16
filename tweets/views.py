from django import forms
from django.forms.utils import ErrorList
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
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super().form_valid(form)
		else:
			form._error[forms.forms.NON_FIELD_ERRORS] = ErrorList("User must be logged in to continue")
			return self.form_invalid(form)
