from rest_framework import serializers
from .models import Ride, RideEvent
from users.models import User
import datetime


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
    ride_events = GetRideEventSerializer(many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    rider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="rider", write_only=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="driver", write_only=True
    )

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
            "ride_events",
            "todays_ride_events",
        )

    def get_todays_ride_events(self, obj):
        todays_events = [
            e for e in obj.ride_events.all()
            if e.created_at.date() == datetime.date.today()
        ]
        return GetRideEventSerializer(todays_events, many=True).data


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

