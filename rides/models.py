from django.db import models
from users.models import User

class Ride(models.Model):
    RIDE_STATUS_CHOICES = (
        ("en-route", "En-Route"),
        ("pickup", "Pickup"),
        ("dropoff", "Dropoff"),
    )

    status = models.CharField(
        choices=RIDE_STATUS_CHOICES,
        default="en-route",
        max_length=20
    )

    rider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rides_as_rider"
    )
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rides_as_driver"
    )

    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)

    pickup_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Ride {self.pk} for {self.rider}"

class RideEvent(models.Model):
    ride = models.ForeignKey(
        Ride, on_delete=models.CASCADE, related_name="ride_events"
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Event for Ride {self.ride.pk}: {self.description}"
