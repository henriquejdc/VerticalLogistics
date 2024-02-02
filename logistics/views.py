# Django imports
import django_filters.rest_framework
from django.db import IntegrityError
from django.http.response import Http404

# Third party imports
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

# Project imports
from shared.helpers import MyCustomPagination
from shared.http.responses import api_exception_response, not_found_response
from shared.views import BaseCollectionViewSet
from logistics.filters import OrderFilter
from logistics.models import Order, UserVL
from logistics.serializers import FileSerializer, UserSerializer, OrderSerializer, OrderSerializerResponse
from logistics.services import create_datadb


class OrderViewSet(BaseCollectionViewSet):
    """ A ViewSet for data. """
    model_class = Order
    queryset = model_class.objects.all()
    pagination_class = MyCustomPagination
    serializer_class = OrderSerializerResponse
    http_method_names = ('get', 'post')
    search_fields = ('name',)
    serializers = {
        'default': serializer_class,
        'create': FileSerializer,
    }
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    filterset_class = OrderFilter
    filterset_fields = (
        'order_id',
        'date__gte',
        'date__lte'
    )
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )

    def response_list(self):
        queryset = self.filter_queryset(self.get_queryset())
        users_queryset = UserVL.objects.filter(
            user_id__in=list(set(queryset.values_list('user', flat=True)))
        ).order_by('user_id')

        page = self.paginate_queryset(users_queryset)

        if page is not None:
            users_queryset = page

        users_data = UserSerializer(users_queryset, many=True).data

        for user_data in users_data:
            user_data['orders'] = OrderSerializer(queryset.filter(user=user_data['user_id']), many=True).data

        return self.get_paginated_response(users_data)

    @swagger_auto_schema(operation_summary="Create objects from file")
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = request.FILES['file']
            create_datadb(file)
            return self.response_list()
        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)
        except IntegrityError as validation_exception:
            return api_exception_response(
                exception=validation_exception,
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="List objects")
    def list(self, request, *args, **kwargs):
        try:
            return self.response_list()
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Retrieve a object")
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_data = UserSerializer(instance.user).data
            user_data['orders'] = OrderSerializer(instance).data
            return Response(user_data)
        except Http404 as exception:
            return not_found_response(exception)
        except Exception as exception:
            return api_exception_response(exception=exception)