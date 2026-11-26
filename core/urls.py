from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("venda-seu-carro/", views.sell_vehicle, name="sell_vehicle"),
]