# Base imports
import django_filters.rest_framework

# Project imports
from logistics.models import Order


class OrderFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    order_id = django_filters.NumberFilter(field_name='order_id', lookup_expr='exact')

    class Meta:
        model = Order
        fields = []
