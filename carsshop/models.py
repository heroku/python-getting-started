from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Car(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    blocked_by_order = models.ForeignKey(
        "Order", on_delete=models.SET_NULL, null=True, related_name="reserved_cars"
    )
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="cars"
    )

    def block(self, order):
        if self.owner:
            raise Exception("Car is already sold")
        if self.blocked_by_order:
            raise Exception("Car is already reserved")
        self.blocked_by_order = order
        self.save()

    def unblock(self):
        self.blocked_by_order = None
        self.save()

    def sell(self):
        if self.owner:
            raise Exception("Car is already sold")
        if not self.blocked_by_order:
            raise Exception("Car is not reserved")
        self.owner = self.blocked_by_order.client
        self.save()

    def __str__(self):
        return self.color


class Licence(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.SET_NULL, null=True, related_name="licence"
    )
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class Dealership(models.Model):
    name = models.CharField(max_length=50)
    available_car_types = models.ManyToManyField(CarType, related_name="dealerships")
    clients = models.ManyToManyField(User, related_name="dealerships")

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    is_paid = models.BooleanField(default=False)

    def add_car_type_to_order(self, car_type, quantity):
        available_cars = Car.objects.filter(
            car_type=car_type, blocked_by_order__isnull=True, owner__isnull=True
        )
        if available_cars.count() >= quantity:
            for _ in range(quantity):
                car = available_cars.first()
                car.block(self)
        else:
            raise Exception("Insufficient cars available for this order")

        OrderQuantity.objects.create(order=self, car_type=car_type, quantity=quantity)

    def cancel_order(self):
        order_quantities = OrderQuantity.objects.filter(order=self)
        for order_quantity in order_quantities:
            car_type = order_quantity.car_type
            quantity = order_quantity.quantity
            cars_to_unblock = Car.objects.filter(
                car_type=car_type, blocked_by_order=self
            )[:quantity]
            for car in cars_to_unblock:
                car.unblock()
            order_quantity.delete()

        self.delete()

    def complete_order(self):
        order_quantities = OrderQuantity.objects.filter(order=self)
        for order_quantity in order_quantities:
            car_type = order_quantity.car_type
            quantity = order_quantity.quantity
            cars_to_sell = Car.objects.filter(car_type=car_type, blocked_by_order=self)[
                :quantity
            ]
            for car in cars_to_sell:
                car.sell()

        self.is_paid = True
        self.save()


class OrderQuantity(models.Model):
    car_type = models.ForeignKey(
        CarType, on_delete=models.CASCADE, related_name="order_quantities"
    )
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="car_types")
