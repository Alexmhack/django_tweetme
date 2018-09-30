from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Tweet

User = get_user_model()

class TweetModelTestCase(TestCase):
	def setUp(self):
		random_user = User.objects.create(username='thisistestuser', password='trydjango')

	def test_tweet_item(self):
		test_obj = Tweet.objects.create(
			user=User.objects.first(),
			content='This is some random test content'
		)

		self.assertTrue(test_obj.content == 'This is some random test content')
		self.assertTrue(test_obj.id == 1)
