from django.urls import path

from .views import (
	TweetDetailView,
	TweetListView,
	TweetCreateView,
	TweetUpdateView,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('tweets/', TweetListView.as_view(), name='tweets'),
	path('create/', TweetCreateView.as_view(), name='create'),
	path('<int:pk>/edit/', TweetUpdateView.as_view(), name='edit'),
]
