from django.urls import path
from .views import BlueprintCreateView, BlueprintDetailView, BlueprintListView, BlueprintUpdateView, BluePrintDeleteView

app_name = "blueprints"
urlpatterns = [
    path('', BlueprintListView.as_view(), name='index'),
    path('create/', BlueprintCreateView.as_view(), name='create'),
    path('<pk>/', BlueprintDetailView.as_view(), name='detail'),
    path('<pk>/edit/', BlueprintUpdateView.as_view(), name='edit'),
    path('<pk>/delete/', BluePrintDeleteView.as_view(), name='delete'),
]