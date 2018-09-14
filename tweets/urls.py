from django.urls import path

from .views import (
	tweet_detail_view,
	tweet_list_view,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:id>/', tweet_detail_view, name='detail'),
	path('tweets/', tweet_list_view, name='tweets'),
]
