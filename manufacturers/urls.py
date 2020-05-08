from django.urls import path
from .views import ManufacturingOrderCreateView, ManufacturingOrderDetailView

app_name = "manufacturers"
urlpatterns = [
    path('create-mo/', ManufacturingOrderCreateView.as_view(), name='create'),
    path('mo/<pk>/', ManufacturingOrderDetailView.as_view(), name='mo_detail'),
]