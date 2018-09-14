from django.urls import path

from .views import (
	tweet_detail_view
)

urlpatterns = [
	path('<int:id>/detail', tweet_detail_view, name='detail'),
]
