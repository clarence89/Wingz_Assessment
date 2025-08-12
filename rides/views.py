from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, ACos

from users.permissions import IsAdminRole
from .models import Ride, RideEvent
from .serializers import RideSerializer, RideEventSerializer
from .filters import RideFilter
import logging

logger = logging.getLogger(__name__)


@swagger_auto_schema(tags=["Rides"])
class RideViewSet(viewsets.ModelViewSet):
    queryset = (
        Ride.objects.select_related("rider", "driver")
        .prefetch_related("ride_events")
        .all()
    )
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ["pickup_time", "distance"]

    def get_queryset(self):
        queryset = super().get_queryset()

        user_latitude = self.request.query_params.get("latitude")
        user_longitude = self.request.query_params.get("longitude")

        if user_latitude and user_longitude:
            try:
                user_latitude = float(user_latitude)
                user_longitude = float(user_longitude)
            except ValueError:
                logger.error("Invalid latitude or longitude format.")
                raise ValueError("Invalid latitude or longitude format.")

            lat1 = Radians(Value(user_latitude))
            lon1 = Radians(Value(user_longitude))
            lat2 = Radians(F("pickup_latitude"))
            lon2 = Radians(F("pickup_longitude"))

            cosine_angle = Cos(lat1) * Cos(lat2) * Cos(lon2 - lon1) + Sin(lat1) * Sin(
                lat2
            )

            distance_expr = ExpressionWrapper(
                6371 * ACos(cosine_angle), output_field=FloatField()
            )

            queryset = queryset.annotate(distance=distance_expr).order_by("distance")

        return queryset


@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = (
        RideEvent.objects.select_related("ride__rider", "ride__driver")
        .all()
    )
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
