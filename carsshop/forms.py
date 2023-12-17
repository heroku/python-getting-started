from django import forms
from .models import CarType, Dealership, Car, Client


class CarTypeForm(forms.ModelForm):
    class Meta:
        model = CarType
        fields = ["name", "brand", "price"]


class DealershipForm(forms.ModelForm):
    class Meta:
        model = Dealership
        fields = ["name", "available_car_types"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["car_type", "color", "year"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
