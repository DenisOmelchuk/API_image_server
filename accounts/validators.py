from django.core.exceptions import ValidationError

def validate_time_to_expired(value):
    """Validates user input of expiration time for link."""
    min_time = 300
    max_time = 30000
    if not min_time <= value <= max_time:
        raise ValidationError("Value must be a number between 300 and 30000 seconds.")