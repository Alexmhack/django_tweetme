from rest_framework import serializers

from tweets.models import Tweet
from accounts.api.serializers import UserModelSerializer

class TweetModelSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	display_date = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()

	class Meta:
		model = Tweet
		fields = [
			'user',
			'content',
			'timestamp',
			'display_date',
			'timesince',
		]

	def get_display_date(self, obj):
		return obj.timestamp.strftime("%b %d at %H:%M %p")

	def get_timesince(self, obj):
		return obj.timestamp
