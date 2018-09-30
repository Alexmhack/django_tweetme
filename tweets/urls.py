from django.urls import path
from django.views.generic.base import RedirectView

from .views import (
	TweetDetailView, TweetListView, TweetCreateView, TweetUpdateView, TweetDeleteView,
)

app_name = 'tweets'

urlpatterns = [
	path('', RedirectView.as_view(url="/", permanent=True)),
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('search/', TweetListView.as_view(), name='list'),
	path('create/', TweetCreateView.as_view(), name='create'),
	path('<int:pk>/edit/', TweetUpdateView.as_view(), name='edit'),
	path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'),
]
