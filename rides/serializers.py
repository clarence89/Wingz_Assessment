from rest_framework import serializers
from .models import Ride, RideEvent
from users.models import User
import datetime

class UserRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class GetRideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    ride_events = GetRideEventSerializer(many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    class Meta:
        model = Ride
        fields = '__all__'
        
    def get_todays_ride_events(self, obj):
        todays_events = obj.ride_events.filter(created_at__date=datetime.date.today())
        return GetRideEventSerializer(todays_events, many=True).data
    
class GetRideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    class Meta:
        model = Ride
        fields = '__all__'

class RideEventSerializer(serializers.ModelSerializer):
    ride = GetRideSerializer(read_only=True)
    class Meta:
        model = RideEvent
        fields = '__all__'