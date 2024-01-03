from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carshop_api.serializers import CarListSerializer, CarTypeSerializer, DealershipSerializer, CarSerializer, \
    OrderSerializer
from carsshop.models import CarType, Dealership, Order, Car, OrderQuantity


# Create your views here.
class CarListView(ListAPIView):
    serializer_class = CarListSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dealerships = Dealership.objects.all()
        dealership_cars_data = []

        for dealership in dealerships:
            dealership_data = {
                'name': dealership.name,
                'available_car_types': CarType.objects.filter(dealerships=dealership).values('id', 'name', 'brand',
                                                                                             'price')
            }
            dealership_cars_data.append(dealership_data)

        order_id = request.user.profile.order_id if hasattr(request.user, 'profile') else 0

        return Response({'dealerships': dealership_cars_data, 'order_id': order_id})

    def post(self, request):
        serializer = CarListSerializer(data=request.data)
        if serializer.is_valid():
            car_type_id = serializer.validated_data['car_type_id']
            quantity = serializer.validated_data['quantity']
            car_type = CarType.objects.get(id=car_type_id)

            client = request.user

            order, created_order = Order.objects.get_or_create(client=client, is_paid=False)
            order.add_car_type_to_order(car_type, quantity)

            client.profile.order_id = order.id
            client.profile.save()

            return redirect('car_list')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCarTypeView(ListAPIView):
    serializer_class = CarTypeSerializer
    queryset = CarType.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        car_type = CarType.objects.all()
        serialized_data = CarTypeSerializer(car_type, many=True).data
        return Response(serialized_data)


class CreateDealershipView(ListAPIView):
    serializer_class = DealershipSerializer
    queryset = Dealership.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DealershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        dealerships = Dealership.objects.all()
        serialized_data = DealershipSerializer(dealerships, many=True).data
        return Response(serialized_data)


class CreateCarView(ListAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        car = Car.objects.all()
        serialized_data = CarSerializer(car, many=True).data
        return Response(serialized_data)


class PaymentView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        if not order.is_paid:
            order.complete_order()
            request.user.profile.order_id = 0
            return Response({"detail": f"Order {order_id} payed success"}, status=status.HTTP_200_OK)

        return Response({"detail": "Order is already paid."}, status=status.HTTP_400_BAD_REQUEST)
