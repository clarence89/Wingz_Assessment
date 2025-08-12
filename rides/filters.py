from django_filters import rest_framework as filters
from .models import Ride

class RideFilter(filters.FilterSet):
    rider_email = filters.CharFilter(field_name='rider__email', lookup_expr='icontains')  # Matches '%...%'

    class Meta:
        model = Ride
        fields = ['rider_email']