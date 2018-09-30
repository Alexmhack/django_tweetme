from django.urls import path

from .views import TweetListAPIView

urlpatterns = [
	path('', TweetListAPIView, name='list')
]
