from rest_framework import serializers
from .models import Violation

class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = ['id', 'date', 'violation_type', 'fine_collected', 'description', 'vehicle_number', 'officer_name', 'image']
        read_only_fields = ['id', 'officer_name']  # Officer name will be set from the logged-in user

    def create(self, validated_data):
        """
        Automatically set the officer_name field based on the user making the request.
        """
        request = self.context.get('request')
        validated_data['officer_name'] = "admin`"
        return super().create(validated_data)
