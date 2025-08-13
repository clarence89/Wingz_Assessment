from rest_framework import serializers
from .models import Ride, RideEvent
from users.models import User
import datetime
from django.utils import timezone

class UserRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role")


class GetRideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ("id", "ride", "description", "created_at")


class RideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    rider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="rider", write_only=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="driver", write_only=True
    )
    distance_m = serializers.FloatField(read_only=True)

    class Meta:
        model = Ride
        fields = (
            "id",
            "status",
            "rider", "rider_id",
            "driver", "driver_id",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "todays_ride_events",
            "distance_m",
        )

    def get_todays_ride_events(self, obj):
        events = getattr(obj, "prefetched_todays_ride_events", None)
        if events is not None:
            return GetRideEventSerializer(events, many=True).data
        
        last_24h = timezone.now() - datetime.timedelta(hours=24)
        events = obj.ride_events.filter(created_at__gte=last_24h)
        return GetRideEventSerializer(events, many=True).data


class GetRideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = (
            "id",
            "status",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
        )


class RideEventSerializer(serializers.ModelSerializer):
    ride = GetRideSerializer(read_only=True)
    ride_id = serializers.PrimaryKeyRelatedField(
        queryset=Ride.objects.all(), source="ride", write_only=True
    )

    class Meta:
        model = RideEvent
        fields = ("id", "ride", "ride_id", "description", "created_at")

