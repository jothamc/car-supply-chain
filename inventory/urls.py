from django.urls import path
from .views import (WholesaleCarDetailView, CarListView, WholesaleCarUpdateView, 
WholesaleCarDeleteView, AllWholesaleCarListView, RetailCarDetailView, RetailCarUpdateView,
RetailCarDeleteView, AllRetailCarListView )

app_name = "inventory"
urlpatterns = [
    path('', CarListView.as_view(), name='index'),
    path('manufacturers/', AllWholesaleCarListView.as_view(), name='manufacturers_inventory'),
    path('wholesale-<pk>/', WholesaleCarDetailView.as_view(), name='wholesale_detail'),
    path('wholesale-<pk>/update/', WholesaleCarUpdateView.as_view(), name='wholesale_update'),
    path('wholesale-<pk>/delete/', WholesaleCarDeleteView.as_view(), name='wholesale_delete'),
    path('retail-<pk>/', RetailCarDetailView.as_view(), name='retail_detail'),
    path('retail-<pk>/update/', RetailCarUpdateView.as_view(), name='retail_update'),
    path('retail-<pk>/delete/', RetailCarDeleteView.as_view(), name='retail_delete'),
    path('dealerships/', AllRetailCarListView.as_view(), name='dealership_inventory'),
]