from django.urls import path
from .views import (WholesaleDealCreateView, WholesaleDealDetailView, WholesaleDealListView, 
acceptWholesaleDeal, rejectWholesaleDeal, RetailDealCreateView, RetailDealDetailView, RetailDealListView,
acceptRetailDeal, rejectRetailDeal, ToDealershipsListView, ToManufacturersListView)

app_name = "deals"
urlpatterns = [
    path('create-wholesale-deal/<pk>/', WholesaleDealCreateView.as_view(), name='wholesale_deal_create'),
    path('from-dealerships/', WholesaleDealListView.as_view(), name='from_dealerships'),
    path('from-dealerships/<pk>/accept/', acceptWholesaleDeal, name='wholesale_deal_accept'),
    path('from-dealerships/<pk>/reject/', rejectWholesaleDeal, name='wholesale_deal_reject'),
    path('wholesale-deal-<pk>/', WholesaleDealDetailView.as_view(), name='wholesale_deal_detail'),
    path('create-retail-deal/<pk>/', RetailDealCreateView.as_view(), name='retail_deal_create'),
    path('retail-deal-<pk>/', RetailDealDetailView.as_view(), name='retail_deal_detail'),
    path('from-customers/', RetailDealListView.as_view(), name='from_customers'),
    path('from-customers/<pk>/accept/', acceptRetailDeal, name='retail_deal_accept'),
    path('from-customers/<pk>/reject/', rejectRetailDeal, name='retail_deal_reject'),

    path('to-dealerships/', ToDealershipsListView.as_view(), name='to_dealerships'),
    path('to-manufacturers/', ToManufacturersListView.as_view(), name='to_manufacturers'),
]