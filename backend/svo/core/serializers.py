from rest_framework import serializers
from push_notifications.api.rest_framework import GCMDeviceSerializer, GCMDevice

from . import models
from .models import ParkingPlace


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Airline
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    estimation = serializers.FloatField(read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "email", "username", "first_name", "last_name", "avatar", "airline", "estimation"]


class ParkingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingPlace
        fields = '__all__'


class CoreResourceSerializer(serializers.ModelSerializer):
    estimation = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Resource
        fields = '__all__'


class CoreApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resource = CoreResourceSerializer(read_only=True)
    parking_place = ParkingPlaceSerializer(read_only=True)

    class Meta:
        model = models.Application
        fields = '__all__'


class FCMDeviceSerializer(GCMDeviceSerializer):

    def create(self, validated_data):
        validated_data['cloud_message_type'] = "FCM"
        instance = GCMDevice.objects.create(
            **validated_data
        )
        return instance