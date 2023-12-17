from django.shortcuts import render, redirect, get_object_or_404

from .forms import DealershipForm, CarTypeForm, CarForm, ClientForm
from .models import CarType, Order, Dealership, Car, Client, OrderQuantity


def car_list(request):
    dealerships = Dealership.objects.all()
    dealership_cars_data = {}

    for dealership in dealerships:
        dealership_cars_data[dealership] = list(dealership.available_car_types.all())

    if request.method == "POST":
        car_type_id = request.POST.get("car_type_id")
        quantity = int(request.POST.get("quantity"))
        car_type = CarType.objects.get(id=car_type_id)

        client, created_client = Client.objects.get_or_create(
            name="Name", email="mail@example.com", phone="+0000000000"
        )  # for test

        order, created_order = Order.objects.get_or_create(client=client, is_paid=False)
        order.add_car_type_to_order(car_type, quantity)

        request.session["order_id"] = order.id
        return redirect("car_list")

    return render(
        request,
        "carshop/car_type_list.html",
        {
            "dealership_cars_data": dealership_cars_data,
            "order_id": request.session.get("order_id", 0),
        },
    )


def create_car_type(request):
    if request.method == "POST":
        form = CarTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_cartype")
    else:
        form = CarTypeForm()

    return render(request, "carshop/create_car_type.html", {"form": form})


def create_dealership(request):
    if request.method == "POST":
        form = DealershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_dealership")
    else:
        form = DealershipForm()

    return render(request, "carshop/create_dealership.html", {"form": form})


def create_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_car")
    else:
        form = CarForm()

    return render(request, "carshop/create_car.html", {"form": form})


def create_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_client")
    else:
        form = ClientForm()

    return render(request, "carshop/create_client.html", {"form": form})


def payment(request, order_id):
    request.session.clear()
    order = get_object_or_404(Order, pk=order_id)
    order_quantities = OrderQuantity.objects.filter(order_id__exact=order_id)
    if request.method == "POST":
        if not order.is_paid:
            order.complete_order()
            request.session["order_id"] = 0
            return redirect("payment_success", order_id=order_id)

    return render(
        request,
        "carshop/payment.html",
        {"order": order, "order_quantities": order_quantities},
    )


def payment_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "carshop/payment_success.html", {"order": order})
