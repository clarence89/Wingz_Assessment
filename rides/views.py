from django.utils import timezone
import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.db.models.expressions import RawSQL

from users.permissions import IsAdminRole
from .models import Ride, RideEvent
from .serializers import RideSerializer, RideEventSerializer
from .filters import RideFilter
import logging

logger = logging.getLogger(__name__)


@swagger_auto_schema(tags=["Rides"])
class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RideFilter

    ordering_fields = ["pickup_time"]
    ordering = ["pickup_time"]
    search_fields = ["rider__email", "driver__email"]

    def get_queryset(self):
        last_24h = timezone.now() - datetime.timedelta(hours=24)
        qs = Ride.objects.select_related("rider", "driver").prefetch_related(
            Prefetch(
                "ride_events",
                queryset=RideEvent.objects.filter(created_at__gte=last_24h),
                to_attr="prefetched_todays_ride_events",
            )
        )

        order_by = self.request.query_params.get("order_by")
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")

        if order_by != "distance":
            return qs

        if not lat or not lng:
            return qs

        try:
            lat_f = float(lat)
            lng_f = float(lng)
        except ValueError:
            return qs

        distance_sql = """
            ST_DistanceSphere(
                ST_MakePoint(%s, %s),
                ST_MakePoint(COALESCE(pickup_longitude, 0), COALESCE(pickup_latitude, 0))
            )
        """
        qs = qs.exclude(pickup_latitude__isnull=True).exclude(
            pickup_longitude__isnull=True
        )
        qs = qs.annotate(distance_m=RawSQL(distance_sql, (lng_f, lat_f)))
        return qs.order_by("distance_m", "id")


@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.select_related("ride__rider", "ride__driver").all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
