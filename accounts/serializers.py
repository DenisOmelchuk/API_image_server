from rest_framework import serializers
from accounts.models import UserImage, ExpiringLink


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['time_to_expired']


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['original_image']


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'  # Include all fields by default

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Remove fields that are not in the "fields" list
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
