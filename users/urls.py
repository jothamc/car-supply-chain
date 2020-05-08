from django.urls import path, include
from .views import UserDetailView, RegisterView, AddBalanceView

app_name = "user"
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('', UserDetailView.as_view(), name="profile"),
    path('register/', RegisterView.as_view(), name="register"),
    path('add-balance', AddBalanceView, name="add_balance"),
]