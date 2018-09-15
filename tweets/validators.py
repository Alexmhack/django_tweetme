from django.core.exceptions import ValidationError

def validate_content(value):
	content = value
	if "fuck" in content:
		raise ValidationError("Cannot have offensive content")

	return value
