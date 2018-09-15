from django.urls import path

from .views import (
	TweetDetailView,
	tweet_list_view,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('tweets/', tweet_list_view, name='tweets'),
]
