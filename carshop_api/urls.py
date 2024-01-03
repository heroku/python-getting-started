from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from carshop_api.views import CarListView, CreateCarTypeView, CreateDealershipView, CreateCarView, PaymentView

urlpatterns = [
    path('car_list/', CarListView.as_view(), name='car_list_api'),
    path('create_car_type/', CreateCarTypeView.as_view(), name='create_car_type_api'),
    path('create_dealership/', CreateDealershipView.as_view(), name='create_dealership_api'),
    path('create_car/', CreateCarView.as_view(), name='create_car_api'),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='payment_api'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
