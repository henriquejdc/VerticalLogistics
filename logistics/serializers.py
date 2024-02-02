# Django imports
from django.db.models import Sum

# Third-party imports
from rest_framework import serializers

# Project imports
from logistics.models import Order, UserVL, Product
from logistics.validators import valid_extension


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserVL
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    value = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_value(self, obj) -> str:
        return str(obj.value)


class OrderSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    products = ProductSerializer(many=True, source='product')

    class Meta:
        model = Order
        fields = (
            'order_id',
            'date',
            'total',
            'products',
        )

    def get_total(self, obj) -> str:
        return str(obj.product.all().aggregate(total=Sum('value'))['total'])


class OrderSerializerResponse(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = UserVL
        fields = (
            'user_id',
            'name',
            'orders',
        )


class FileSerializer(serializers.Serializer):

    file = serializers.FileField(
        required=True,
        validators=[valid_extension],
    )
