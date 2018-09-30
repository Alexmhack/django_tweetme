from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name'
		]
