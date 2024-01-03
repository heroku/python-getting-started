from django.contrib.auth.models import User
from rest_framework import serializers

from carsshop.models import Client, CarType, Car, Licence, Dealership, Order, OrderQuantity


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = ('number',)


class CarSerializer(serializers.ModelSerializer):
    licence = LicenceSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'car_type', 'color', 'year', 'blocked_by_order', 'owner', 'licence')


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ('id', 'name', 'brand', 'price')


class DealershipSerializer(serializers.ModelSerializer):
    available_car_types = CarTypeSerializer(many=True)

    class Meta:
        model = Dealership
        fields = ('id', 'name', 'available_car_types')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class OrderQuantitySerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer()

    class Meta:
        model = OrderQuantity
        fields = ('id', 'car_type', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    car_types = OrderQuantitySerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'is_paid', 'car_types')


class CarListSerializer(serializers.Serializer):
    car_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


