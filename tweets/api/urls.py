from django.urls import path

from .views import TweetListAPIView

app_name = 'tweets-api'

urlpatterns = [
	path('', TweetListAPIView, name='list')
]
