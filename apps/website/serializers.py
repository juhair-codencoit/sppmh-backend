from rest_framework import serializers
from .models import *


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name', 'created_at', 'updated_at']

        read_only_fields = ['created_at', 'updated_at']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    
class UserRegistrationSerializer(serializers.ModelSerializer):
    batch_id = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all(), source='batch', write_only=True)
    batch = BatchSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'batch_id','batch', 'phone_number', 'country_code',
                  'dob', 'blood_group', 'current_city', 'workplace', 'position', 'is_external', 'image', 'cv']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if instance.image and hasattr(instance.image, 'url'):
            representation['image'] = request.build_absolute_uri(instance.image.url)
        else:
            representation['image'] = None

        if instance.cv and hasattr(instance.cv, 'url'):
            representation['cv'] = request.build_absolute_uri(instance.cv.url)
        else:
            representation['cv'] = None

        return representation
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        batch = validated_data.pop('batch', None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.batch = batch
        user.save()
        return user

