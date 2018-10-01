from rest_framework import generics
from rest_framework import permissions

from django.db.models import Q

from tweets.models import Tweet
from .serializers import TweetModelSerializer

class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer

	def get_queryset(self):
		qs = Tweet.objects.all().order_by("-timestamp")
		query = self.request.GET.get("q", None)
		print(self.request.GET)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
			)
		return qs


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
