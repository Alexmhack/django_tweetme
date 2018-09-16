from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserTweetMixin

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	template_name = "tweets/list_view.html"

	def get_queryset(self):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		print(self.request.GET)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
			)
		return qs


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	login_url = "/admin"


class TweetUpdateView(LoginRequiredMixin, UserTweetMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"


class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	success_url = reverse_lazy("tweets:delete")
