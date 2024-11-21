from django.urls import path
from mtn_test import views


urlpatterns = [
    path('', views.home, name="Home"),
    path('checkout/<int:route_id>/', views.checkout, name="checkout"),
    path("pay/<int:route_id>/", views.initiate_payment, name="initiate_payment"),
]
